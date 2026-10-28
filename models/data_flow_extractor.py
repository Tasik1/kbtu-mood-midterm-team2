"""
Data Flow Graph (DFG) Extractor for Java Source Code.
Course: Management of Organizational Data (MoOD) 2026 - Master's Programme
Team 2: Bidaishiev Shyntas, Ibragim Anzir, Ardak Aruzhan, Amanbayev Farkhad

Implements Data Flow Graph extraction aligned with GraphCodeBERT (Guo et al., ICLR 2021):
- Identifies variable declarations and formal parameters
- Extracts variable definitions (assignments, initializations)
- Tracks variable usages (conditions, function calls, return statements)
- Builds def-use edges: (var_def -> var_use)
- Constructs node sequences and adjacency / attention masks
"""

import re
from typing import List, Tuple, Dict, Set, Any
import numpy as np

# Standard Java keywords and primitive types to distinguish identifiers from language constructs
JAVA_KEYWORDS = {
    "abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class",
    "const", "continue", "default", "do", "double", "else", "enum", "extends", "final",
    "finally", "float", "for", "goto", "if", "implements", "import", "instanceof", "int",
    "interface", "long", "native", "new", "package", "private", "protected", "public",
    "return", "short", "static", "strictfp", "super", "switch", "synchronized", "this",
    "throw", "throws", "transient", "try", "void", "volatile", "while", "true", "false",
    "null", "String", "Object", "List", "Map", "Set", "Integer", "Boolean", "Long"
}

class JavaDataFlowExtractor:
    def __init__(self, max_dfg_nodes: int = 32):
        self.max_dfg_nodes = max_dfg_nodes

    def tokenize_code(self, code: str) -> List[str]:
        """Tokenizes Java code into symbols, keywords, identifiers, and literals."""
        # Regex to split on identifiers, numbers, operators, punctuation
        pattern = r'[a-zA-Z_][a-zA-Z0-9_]*|\d+|==|!=|<=|>=|&&|\|\||\+\+|--|\+=|-=|\*=|/=|->|::|[{}()\[\];,.<>+*/%&|^!~?:=-]'
        tokens = re.findall(pattern, code)
        return tokens

    def extract_variables_and_dfg(self, code: str) -> Dict[str, Any]:
        """
        Extracts variable nodes and def-use edges from Java source code.
        Returns:
            - 'tokens': List of code tokens
            - 'dfg_nodes': List of variable identifier strings
            - 'dfg_edges': List of (source_idx, target_idx) pairs representing def->use dependencies
            - 'adjacency_matrix': (K x K) binary numpy array where K = len(dfg_nodes)
            - 'code_dfg_alignment': List of (code_token_idx, dfg_node_idx) alignments
        """
        tokens = self.tokenize_code(code)
        
        # Identify candidate variable identifiers (non-keyword identifiers)
        candidate_vars: List[Tuple[int, str]] = [] # (token_idx, var_name)
        for i, t in enumerate(tokens):
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', t) and t not in JAVA_KEYWORDS:
                # filter out method declarations followed immediately by '(' when preceded by visibility/type
                # keep variables
                candidate_vars.append((i, t))

        # Track definitions vs uses
        defs: Dict[str, List[int]] = {}
        uses: Dict[str, List[int]] = {}
        dfg_nodes: List[str] = []
        var_to_node_idx: Dict[str, int] = {}

        # Scan tokens for assignment patterns:
        # e.g.: type var = expr; var = expr; for (int i = 0; ...); func(param)
        for idx, (tok_idx, var_name) in enumerate(candidate_vars):
            if var_name not in var_to_node_idx:
                if len(dfg_nodes) < self.max_dfg_nodes:
                    var_to_node_idx[var_name] = len(dfg_nodes)
                    dfg_nodes.append(var_name)
                    defs[var_name] = []
                    uses[var_name] = []

            # Check if this occurrence is a definition or use
            next_token = tokens[tok_idx + 1] if tok_idx + 1 < len(tokens) else ""
            prev_token = tokens[tok_idx - 1] if tok_idx > 0 else ""

            is_def = False
            if next_token in ("=", "+=", "-=", "*=", "/="):
                is_def = True
            elif prev_token in ("int", "long", "float", "double", "byte", "short", "char", "boolean", "String", "final"):
                is_def = True

            if var_name in var_to_node_idx:
                if is_def:
                    defs[var_name].append(tok_idx)
                else:
                    uses[var_name].append(tok_idx)

        # Build def-use edges
        dfg_edges: List[Tuple[int, int]] = []
        k = len(dfg_nodes)
        adj = np.eye(k, dtype=np.float32) # self-loops

        for var_name, node_i in var_to_node_idx.items():
            var_defs = defs.get(var_name, [])
            var_uses = uses.get(var_name, [])
            
            # If variable has defs and uses, connect them
            if var_defs and var_uses:
                # Sequential data flow: connect each def to subsequent uses
                for d in var_defs:
                    for u in var_uses:
                        if u > d:
                            dfg_edges.append((node_i, node_i))
                            adj[node_i, node_i] = 1.0

        # Also connect related variables that appear in the same assignment statement:
        # e.g., result = handle(response); -> edge from response to result
        for i, tok in enumerate(tokens):
            if tok == "=" and i > 0 and i + 1 < len(tokens):
                lhs = tokens[i - 1]
                # scan right side up to ';'
                rhs_tokens = []
                for j in range(i + 1, min(len(tokens), i + 25)):
                    if tokens[j] in (";", ","):
                        break
                    rhs_tokens.append(tokens[j])
                
                if lhs in var_to_node_idx:
                    lhs_node = var_to_node_idx[lhs]
                    for r in rhs_tokens:
                        if r in var_to_node_idx and r != lhs:
                            rhs_node = var_to_node_idx[r]
                            dfg_edges.append((rhs_node, lhs_node))
                            adj[rhs_node, lhs_node] = 1.0

        # Code-DFG alignments
        alignments: List[Tuple[int, int]] = []
        for tok_idx, var_name in candidate_vars:
            if var_name in var_to_node_idx:
                alignments.append((tok_idx, var_to_node_idx[var_name]))

        return {
            "tokens": tokens,
            "dfg_nodes": dfg_nodes,
            "dfg_edges": dfg_edges,
            "adjacency_matrix": adj,
            "alignments": alignments,
            "num_nodes": len(dfg_nodes),
            "num_edges": len(dfg_edges)
        }

if __name__ == "__main__":
    extractor = JavaDataFlowExtractor()
    sample_code = """
    public String sanitizeInput(String userInput) {
        String clean = userInput.trim();
        if (clean.contains("<script>")) {
            clean = clean.replace("<script>", "");
        }
        return clean;
    }
    """
    res = extractor.extract_variables_and_dfg(sample_code)
    print("Tokens:", len(res["tokens"]))
    print("DFG Nodes (Variables):", res["dfg_nodes"])
    print("DFG Edges (Def-Use):", res["dfg_edges"])
    print("Adjacency shape:", res["adjacency_matrix"].shape)
