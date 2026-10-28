"""
Primary Method: GraphCodeBERT + Data Flow Classifier.
Course: Management of Organizational Data (MoOD) 2026 - Master's Programme
Team 2: Bidaishiev Shyntas, Ibragim Anzir, Ardak Aruzhan, Amanbayev Farkhad

Architecture:
- Base: microsoft/graphcodebert-base (Transformer encoder with code and graph pre-training)
- Graph Attention Pooling: aggregates variable representations guided by Def-Use Adjacency
- Multi-representation fusion: [CLS, Mean-Code-Embedding, DFG-Attention-Embedding]
- Classification Head: LayerNorm -> Linear(3D -> D) -> GELU -> Dropout -> Linear(D -> 2)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer
from typing import Dict, Tuple, Optional

class GraphAttentionLayer(nn.Module):
    """
    Graph Attention layer that computes attention over data-flow variable nodes
    constrained by the adjacency matrix (def-use relations).
    """
    def __init__(self, hidden_dim: int, num_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = hidden_dim // num_heads
        self.scale = self.head_dim ** -0.5
        
        self.q_proj = nn.Linear(hidden_dim, hidden_dim)
        self.k_proj = nn.Linear(hidden_dim, hidden_dim)
        self.v_proj = nn.Linear(hidden_dim, hidden_dim)
        self.out_proj = nn.Linear(hidden_dim, hidden_dim)
        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(hidden_dim)

    def forward(self, nodes: torch.Tensor, adj_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        nodes: [B, K, D] where K is number of DFG nodes
        adj_mask: [B, K, K] where 1.0 means edge exists, 0.0 means disconnected
        """
        B, K, D = nodes.shape
        residual = nodes

        q = self.q_proj(nodes).view(B, K, self.num_heads, self.head_dim).transpose(1, 2) # [B, H, K, d]
        k = self.k_proj(nodes).view(B, K, self.num_heads, self.head_dim).transpose(1, 2) # [B, H, K, d]
        v = self.v_proj(nodes).view(B, K, self.num_heads, self.head_dim).transpose(1, 2) # [B, H, K, d]

        scores = torch.matmul(q, k.transpose(-2, -1)) * self.scale # [B, H, K, K]

        if adj_mask is not None:
            # adj_mask: [B, K, K] -> [B, 1, K, K]
            mask = (1.0 - adj_mask.unsqueeze(1)) * -1e9
            scores = scores + mask

        attn_weights = F.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)

        context = torch.matmul(attn_weights, v) # [B, H, K, d]
        context = context.transpose(1, 2).contiguous().view(B, K, D)
        out = self.out_proj(context)
        return self.norm(residual + out)

class GraphCodeBERTDataFlowClassifier(nn.Module):
    """
    End-to-End Vulnerability Classifier fusing contextual code representations
    with structural data-flow graph semantics.
    """
    def __init__(
        self,
        model_name: str = "microsoft/graphcodebert-base",
        num_classes: int = 2,
        dropout_prob: float = 0.2,
        freeze_encoder: bool = False
    ):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        self.hidden_dim = self.encoder.config.hidden_size

        if freeze_encoder:
            for param in self.encoder.parameters():
                param.requires_grad = False

        self.dfg_attention = GraphAttentionLayer(self.hidden_dim, num_heads=4, dropout=dropout_prob)
        
        # Classification head combining CLS (D) + mean code (D) + dfg pooled (D) = 3 * D
        self.norm = nn.LayerNorm(self.hidden_dim * 3)
        self.dense = nn.Linear(self.hidden_dim * 3, self.hidden_dim)
        self.activation = nn.GELU()
        self.dropout = nn.Dropout(dropout_prob)
        self.classifier = nn.Linear(self.hidden_dim, num_classes)

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        dfg_node_indices: Optional[torch.Tensor] = None, # [B, K]
        dfg_adj: Optional[torch.Tensor] = None,          # [B, K, K]
        labels: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        sequence_output = outputs.last_hidden_state # [B, L, D]
        cls_rep = sequence_output[:, 0, :]          # [B, D]

        # Mean-pooled code representation (excluding padding)
        expanded_mask = attention_mask.unsqueeze(-1).expand_as(sequence_output)
        sum_embeddings = torch.sum(sequence_output * expanded_mask, dim=1)
        sum_mask = torch.clamp(expanded_mask.sum(dim=1), min=1e-9)
        code_rep = sum_embeddings / sum_mask        # [B, D]

        # DFG representations
        if dfg_node_indices is not None and dfg_node_indices.size(1) > 0:
            B, K = dfg_node_indices.shape
            batch_idx = torch.arange(B, device=input_ids.device).unsqueeze(1).expand(B, K)
            # clamp indices to sequence length
            valid_indices = torch.clamp(dfg_node_indices, 0, sequence_output.size(1) - 1)
            dfg_node_embeds = sequence_output[batch_idx, valid_indices] # [B, K, D]
            dfg_refined = self.dfg_attention(dfg_node_embeds, dfg_adj)
            dfg_rep = torch.mean(dfg_refined, dim=1)                    # [B, D]
        else:
            dfg_rep = code_rep

        fusion = torch.cat([cls_rep, code_rep, dfg_rep], dim=-1)       # [B, 3 * D]
        fusion = self.norm(fusion)
        hidden = self.dropout(self.activation(self.dense(fusion)))
        logits = self.classifier(hidden)                                # [B, 2]

        loss = None
        if labels is not None:
            loss = F.cross_entropy(logits, labels)

        return {
            "loss": loss,
            "logits": logits,
            "probabilities": F.softmax(logits, dim=-1),
            "cls_embedding": cls_rep,
            "fusion_embedding": fusion
        }
