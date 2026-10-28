"""
Unified Training, Evaluation, and Visualization Pipeline.
Course: Management of Organizational Data (MoOD) 2026 - Master's Programme
Team 2: Bidaishiev Shyntas, Ibragim Anzir, Ardak Aruzhan, Amanbayev Farkhad

Assigned Topic:
- Primary Method: GraphCodeBERT + Data Flow Classifier
- Alternative Method: GraphCodeBERT + Frozen Embeddings + Random Forest
Evaluation Criteria: Accuracy (target >= 93%), Precision, Recall, F1, ROC-AUC, Confusion Matrix.
"""

import os
import sys
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("midterm"))

import json
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Any

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)
from transformers import AutoTokenizer

from models.data_flow_extractor import JavaDataFlowExtractor
from models.graphcodebert_classifier import GraphCodeBERTDataFlowClassifier
from models.alternative_classifier import GraphCodeBERTRandomForest

# Set random seeds for reproducibility
def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

class JavaVulnerabilityDataset(Dataset):
    def __init__(
        self,
        jsonl_path: str,
        tokenizer,
        max_length: int = 256,
        max_dfg_nodes: int = 16
    ):
        self.data = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    self.data.append(json.loads(line.strip()))

        self.tokenizer = tokenizer
        self.max_length = max_length
        self.max_dfg_nodes = max_dfg_nodes
        self.extractor = JavaDataFlowExtractor(max_dfg_nodes=max_dfg_nodes)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        code = item["code"]
        target = item["target"]

        # Extract DFG
        dfg_info = self.extractor.extract_variables_and_dfg(code)
        tokens = dfg_info["tokens"]
        dfg_nodes = dfg_info["dfg_nodes"]
        adj = dfg_info["adjacency_matrix"]

        # Tokenize code with special tokens
        encoding = self.tokenizer(
            code,
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        )
        input_ids = encoding["input_ids"].squeeze(0)
        attention_mask = encoding["attention_mask"].squeeze(0)

        # Pad or truncate DFG nodes and adjacency
        k = len(dfg_nodes)
        dfg_indices = []
        for var in dfg_nodes:
            # find first occurrence in input_ids
            var_token_ids = self.tokenizer.encode(var, add_special_tokens=False)
            found_idx = 0
            if var_token_ids:
                matches = (input_ids == var_token_ids[0]).nonzero(as_tuple=True)[0]
                if len(matches) > 0:
                    found_idx = matches[0].item()
            dfg_indices.append(found_idx)

        # Pad DFG indices to max_dfg_nodes
        padded_indices = np.zeros(self.max_dfg_nodes, dtype=np.int64)
        padded_adj = np.eye(self.max_dfg_nodes, dtype=np.float32)

        actual_k = min(k, self.max_dfg_nodes)
        if actual_k > 0:
            padded_indices[:actual_k] = dfg_indices[:actual_k]
            padded_adj[:actual_k, :actual_k] = adj[:actual_k, :actual_k]

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "dfg_node_indices": torch.tensor(padded_indices, dtype=torch.long),
            "dfg_adj": torch.tensor(padded_adj, dtype=torch.float32),
            "target": torch.tensor(target, dtype=torch.long)
        }

def generate_visualizations(
    metrics_primary: Dict[str, Any],
    metrics_alt: Dict[str, Any],
    output_dir: str = "midterm/results"
):
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # 1. Confusion Matrix for Primary Method
    plt.figure(figsize=(6, 5))
    cm_p = np.array(metrics_primary["confusion_matrix"])
    sns.heatmap(cm_p, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Non-Vulnerable (0)", "Vulnerable (1)"],
                yticklabels=["Non-Vulnerable (0)", "Vulnerable (1)"])
    plt.title("Primary Method: GraphCodeBERT + Data Flow Classifier\nConfusion Matrix", fontsize=12, fontweight="bold")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "confusion_matrix_primary.png"), dpi=300)
    plt.close()

    # 2. Confusion Matrix for Alternative Method
    plt.figure(figsize=(6, 5))
    cm_a = np.array(metrics_alt["confusion_matrix"])
    sns.heatmap(cm_a, annot=True, fmt="d", cmap="Greens", cbar=False,
                xticklabels=["Non-Vulnerable (0)", "Vulnerable (1)"],
                yticklabels=["Non-Vulnerable (0)", "Vulnerable (1)"])
    plt.title("Alternative Method: GraphCodeBERT + Random Forest\nConfusion Matrix", fontsize=12, fontweight="bold")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "confusion_matrix_alternative.png"), dpi=300)
    plt.close()

    # 3. ROC Curves Comparison
    plt.figure(figsize=(7, 6))
    fpr_p, tpr_p, _ = roc_curve(metrics_primary["true_labels"], metrics_primary["probabilities"])
    fpr_a, tpr_a, _ = roc_curve(metrics_alt["true_labels"], metrics_alt["probabilities"])
    plt.plot(fpr_p, tpr_p, color="#1f77b4", lw=2.5,
             label=f'Primary: GraphCodeBERT+DFG (AUC = {metrics_primary["roc_auc"]:.4f})')
    plt.plot(fpr_a, tpr_a, color="#2ca02c", lw=2, linestyle="--",
             label=f'Alternative: Frozen+RF (AUC = {metrics_alt["roc_auc"]:.4f})')
    plt.plot([0, 1], [0, 1], color="grey", lw=1.5, linestyle=":")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate (1 - Specificity)", fontsize=11)
    plt.ylabel("True Positive Rate (Recall / Sensitivity)", fontsize=11)
    plt.title("Receiver Operating Characteristic (ROC) Comparison", fontsize=13, fontweight="bold")
    plt.legend(loc="lower right", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "roc_curve_comparison.png"), dpi=300)
    plt.close()

    # 4. Metrics Comparison Bar Chart
    plt.figure(figsize=(8, 5))
    metrics_names = ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    vals_p = [metrics_primary["accuracy"], metrics_primary["precision"], metrics_primary["recall"],
              metrics_primary["f1_score"], metrics_primary["roc_auc"]]
    vals_a = [metrics_alt["accuracy"], metrics_alt["precision"], metrics_alt["recall"],
              metrics_alt["f1_score"], metrics_alt["roc_auc"]]

    x = np.arange(len(metrics_names))
    width = 0.35
    plt.bar(x - width/2, vals_p, width, label="Primary: GraphCodeBERT + DFG", color="#2b5c8f")
    plt.bar(x + width/2, vals_a, width, label="Alternative: Frozen + RF", color="#4ba173")

    plt.axhline(y=0.93, color="crimson", linestyle="--", lw=1.5, label="Requirement Threshold (93%)")
    plt.ylabel("Score", fontsize=11)
    plt.title("Evaluation Metrics: Primary vs. Alternative Method", fontsize=13, fontweight="bold")
    plt.xticks(x, metrics_names, fontsize=11)
    plt.ylim(0.70, 1.02)
    for i in range(len(metrics_names)):
        plt.text(x[i] - width/2, vals_p[i] + 0.01, f"{vals_p[i]*100:.1f}%", ha='center', fontsize=9, fontweight='bold')
        plt.text(x[i] + width/2, vals_a[i] + 0.01, f"{vals_a[i]*100:.1f}%", ha='center', fontsize=9)
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "metrics_barchart.png"), dpi=300)
    plt.close()

    # 5. Data Lifecycle Diagram
    fig, ax = plt.subplots(figsize=(12, 4))
    stages = [
        "1. Acquisition\n(Git Commits)",
        "2. Validation\n(Schema & AST)",
        "3. Storage\n(Clean JSONL)",
        "4. Transform\n(DFG Extraction)",
        "5. Training\n(GraphCodeBERT)",
        "6. Evaluation\n(>=93% Acc Target)",
        "7. Retention\n(Audit & Archive)"
    ]
    ax.axis("off")
    for i, s in enumerate(stages):
        ax.annotate(
            s, xy=(i * 1.8 + 0.9, 0.5), xycoords='data',
            bbox=dict(boxstyle="round,pad=0.6", fc="#e1f0fc", ec="#1b6ca8", lw=2),
            ha="center", va="center", fontsize=10, fontweight="bold"
        )
        if i < len(stages) - 1:
            ax.annotate("", xy=((i+1)*1.8, 0.5), xytext=(i*1.8 + 1.8, 0.5),
                        arrowprops=dict(arrowstyle="->", lw=2.5, color="#1b6ca8"))
    plt.title("Organizational Data Lifecycle (Lecture 1 — DAMA-DMBOK Aligned)", fontsize=13, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "data_lifecycle_diagram.png"), dpi=300)
    plt.close()

    # 6. System Architecture Diagram
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.axis("off")
    # Draw architecture blocks
    boxes = [
        ("Java Source Code\n(Functions & CWEs)", 0.1, 0.65, 0.2, 0.25, "#e8f4f8"),
        ("DFG Extractor\n(Def-Use Chains)", 0.1, 0.2, 0.2, 0.25, "#e8f4f8"),
        ("GraphCodeBERT Encoder\n(Code Tokens + Variable Nodes)", 0.4, 0.425, 0.25, 0.35, "#d1e7dd"),
        ("Graph Attention Pooling\n(Adjacency-Guided)", 0.72, 0.65, 0.24, 0.25, "#fff3cd"),
        ("Frozen + Random Forest\n(Alternative)", 0.72, 0.2, 0.24, 0.25, "#f8d7da"),
        ("Decision: Vulnerable / Secure", 0.72, 0.02, 0.24, 0.12, "#d4edda")
    ]
    for text, x_b, y_b, w_b, h_b, color in boxes:
        rect = plt.Rectangle((x_b, y_b), w_b, h_b, facecolor=color, edgecolor="#333", lw=1.8,
                              transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(x_b + w_b/2, y_b + h_b/2, text, transform=ax.transAxes,
                ha='center', va='center', fontsize=9.5, fontweight='bold')

    # Connections
    ax.annotate("", xy=(0.39, 0.6), xytext=(0.31, 0.75), xycoords='axes fraction', arrowprops=dict(arrowstyle="->", lw=2, color="#333"))
    ax.annotate("", xy=(0.39, 0.55), xytext=(0.31, 0.35), xycoords='axes fraction', arrowprops=dict(arrowstyle="->", lw=2, color="#333"))
    ax.annotate("", xy=(0.71, 0.75), xytext=(0.66, 0.65), xycoords='axes fraction', arrowprops=dict(arrowstyle="->", lw=2, color="#333"))
    ax.annotate("", xy=(0.71, 0.35), xytext=(0.66, 0.5), xycoords='axes fraction', arrowprops=dict(arrowstyle="->", lw=2, color="#333"))
    ax.annotate("", xy=(0.84, 0.15), xytext=(0.84, 0.64), xycoords='axes fraction', arrowprops=dict(arrowstyle="->", lw=2, color="#333"))

    plt.title("Intelligent Vulnerability Detection System Architecture\n(Team 2: GraphCodeBERT + Data Flow Classifier)",
              fontsize=13, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "architecture_diagram.png"), dpi=300)
    plt.close()
    print(f"[Visualization] All 6 publication-quality diagrams generated in {output_dir}")

def run_pipeline():
    set_seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Device] Using compute device: {device}")

    # Load cleaned data
    train_path = "midterm/data/processed/train_cleaned.jsonl"
    valid_path = "midterm/data/processed/valid_cleaned.jsonl"
    test_path = "midterm/data/processed/test_cleaned.jsonl"

    model_name = "microsoft/graphcodebert-base"
    print(f"[Tokenizer] Loading tokenizer for {model_name}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    except Exception as e:
        print(f"[Tokenizer] Direct load failed ({e}), using fallback roberta-base")
        tokenizer = AutoTokenizer.from_pretrained("roberta-base")

    train_dataset = JavaVulnerabilityDataset(train_path, tokenizer, max_length=256, max_dfg_nodes=16)
    valid_dataset = JavaVulnerabilityDataset(valid_path, tokenizer, max_length=256, max_dfg_nodes=16)
    test_dataset = JavaVulnerabilityDataset(test_path, tokenizer, max_length=256, max_dfg_nodes=16)

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    valid_loader = DataLoader(valid_dataset, batch_size=16, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

    print(f"[Dataset] Train: {len(train_dataset)}, Valid: {len(valid_dataset)}, Test: {len(test_dataset)}")

    # 1. Primary Model: GraphCodeBERT + Data Flow Classifier
    print("\n" + "="*60)
    print("PRIMARY METHOD: GraphCodeBERT + Data Flow Classifier")
    print("="*60)
    model = GraphCodeBERTDataFlowClassifier(model_name=model_name, num_classes=2, dropout_prob=0.2)
    model.to(device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)
    criterion = nn.CrossEntropyLoss()

    best_val_acc = 0.0
    best_model_path = "midterm/models/best_graphcodebert_dfg.pt"

    # Training epochs
    epochs = 5
    for epoch in range(1, epochs + 1):
        model.train()
        total_train_loss = 0.0
        for batch in train_loader:
            optimizer.zero_grad()
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            dfg_indices = batch["dfg_node_indices"].to(device)
            dfg_adj = batch["dfg_adj"].to(device)
            targets = batch["target"].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                dfg_node_indices=dfg_indices,
                dfg_adj=dfg_adj,
                labels=targets
            )
            loss = outputs["loss"]
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            total_train_loss += loss.item()

        avg_train_loss = total_train_loss / len(train_loader)

        # Validation
        model.eval()
        val_preds, val_targets = [], []
        with torch.no_grad():
            for batch in valid_loader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                dfg_indices = batch["dfg_node_indices"].to(device)
                dfg_adj = batch["dfg_adj"].to(device)
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    dfg_node_indices=dfg_indices,
                    dfg_adj=dfg_adj
                )
                preds = torch.argmax(outputs["logits"], dim=-1).cpu().numpy()
                val_preds.extend(preds)
                val_targets.extend(batch["target"].numpy())

        val_acc = accuracy_score(val_targets, val_preds)
        print(f"Epoch {epoch}/{epochs} | Train Loss: {avg_train_loss:.4f} | Val Accuracy: {val_acc:.4f}")
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), best_model_path)

    # Load best checkpoint for evaluation
    if os.path.exists(best_model_path):
        model.load_state_dict(torch.load(best_model_path))

    # Evaluate Primary on Test Set
    model.eval()
    test_preds, test_probs, test_targets = [], [], []
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            dfg_indices = batch["dfg_node_indices"].to(device)
            dfg_adj = batch["dfg_adj"].to(device)
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                dfg_node_indices=dfg_indices,
                dfg_adj=dfg_adj
            )
            probs = outputs["probabilities"][:, 1].cpu().numpy()
            preds = torch.argmax(outputs["logits"], dim=-1).cpu().numpy()
            test_preds.extend(preds)
            test_probs.extend(probs)
            test_targets.extend(batch["target"].numpy())

    primary_acc = accuracy_score(test_targets, test_preds)
    primary_prec = precision_score(test_targets, test_preds, zero_division=0)
    primary_rec = recall_score(test_targets, test_preds, zero_division=0)
    primary_f1 = f1_score(test_targets, test_preds, zero_division=0)
    primary_auc = roc_auc_score(test_targets, test_probs)
    primary_cm = confusion_matrix(test_targets, test_preds).tolist()

    metrics_primary = {
        "model": "GraphCodeBERT + Data Flow Classifier",
        "accuracy": round(float(primary_acc), 4),
        "precision": round(float(primary_prec), 4),
        "recall": round(float(primary_rec), 4),
        "f1_score": round(float(primary_f1), 4),
        "roc_auc": round(float(primary_auc), 4),
        "confusion_matrix": primary_cm,
        "true_labels": [int(x) for x in test_targets],
        "predictions": [int(x) for x in test_preds],
        "probabilities": [float(x) for x in test_probs]
    }

    # 2. Alternative Method: GraphCodeBERT + Frozen Embeddings + Random Forest
    print("\n" + "="*60)
    print("ALTERNATIVE METHOD: GraphCodeBERT + Frozen Embeddings + Random Forest")
    print("="*60)
    
    # Extract frozen embeddings from encoder
    def extract_features(loader):
        feats = []
        targets = []
        with torch.no_grad():
            for batch in loader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                dfg_indices = batch["dfg_node_indices"].to(device)
                dfg_adj = batch["dfg_adj"].to(device)
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    dfg_node_indices=dfg_indices,
                    dfg_adj=dfg_adj
                )
                feats.append(outputs["fusion_embedding"].cpu().numpy())
                targets.extend(batch["target"].numpy())
        return np.vstack(feats), np.array(targets)

    X_train, y_train = extract_features(train_loader)
    X_test, y_test = extract_features(test_loader)

    rf_model = GraphCodeBERTRandomForest(n_estimators=300, max_depth=16, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_eval = rf_model.evaluate(X_test, y_test)
    rf_model.save("midterm/models/random_forest_alternative.joblib")

    metrics_alt = {
        "model": "GraphCodeBERT + Frozen Embeddings + Random Forest",
        "accuracy": rf_eval["accuracy"],
        "precision": rf_eval["precision"],
        "recall": rf_eval["recall"],
        "f1_score": rf_eval["f1_score"],
        "roc_auc": rf_eval["roc_auc"],
        "confusion_matrix": rf_eval["confusion_matrix"],
        "true_labels": [int(x) for x in y_test],
        "predictions": rf_eval["predictions"],
        "probabilities": rf_eval["probabilities"]
    }

    # Save summary
    summary_path = "midterm/results/metrics_summary.json"
    full_results = {
        "team": "Team 2",
        "members": [
            {"name": "Bidaishiev Shyntas", "student_id": "25MD0291"},
            {"name": "Ibragim Anzir", "student_id": "25MD0311"},
            {"name": "Ardak Aruzhan", "student_id": "25MD0308"},
            {"name": "Amanbayev Farkhad", "student_id": "25MD0304"}
        ],
        "primary_method": metrics_primary,
        "alternative_method": metrics_alt,
        "requirements_met": {
            "accuracy_ge_93": metrics_primary["accuracy"] >= 0.93,
            "data_flow_utilized": True,
            "alternative_evaluated": True
        }
    }

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(full_results, f, indent=2)

    print(f"\n[Results] Saved metrics summary to {summary_path}")
    print(f"Primary Model Accuracy: {metrics_primary['accuracy'] * 100:.2f}% | F1: {metrics_primary['f1_score']:.4f} | AUC: {metrics_primary['roc_auc']:.4f}")
    print(f"Alternative Model Accuracy: {metrics_alt['accuracy'] * 100:.2f}% | F1: {metrics_alt['f1_score']:.4f} | AUC: {metrics_alt['roc_auc']:.4f}")

    # Generate visualizations
    generate_visualizations(metrics_primary, metrics_alt)

if __name__ == "__main__":
    run_pipeline()
