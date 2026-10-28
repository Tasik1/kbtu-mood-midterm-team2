"""
Generates the comprehensive Jupyter Notebook for Team 2 Midterm.
Course: Management of Organizational Data (MoOD) 2026 - Master's Programme
Team 2: Bidaishiev Shyntas, Ibragim Anzir, Ardak Aruzhan, Amanbayev Farkhad
"""

import json
import os

def create_notebook():
    nb = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    def add_md(source):
        nb["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [s + "\n" for s in source.split("\n")]
        })

    def add_code(source):
        nb["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [s + "\n" for s in source.split("\n")]
        })

    # Cell 1: Title
    add_md("""# Kazakh-British Technical University (KBTU)
## Master's Programme — Management of Organizational Data (MoOD) 2026
### Midterm Group Project: Java Source Code Vulnerability Detection
---
**Team**: Group 2  
**Assigned Method**: GraphCodeBERT + Data Flow Classifier  
**Alternative Method**: GraphCodeBERT + Frozen Embeddings + Random Forest  
**Repository**: [https://github.com/Tasik1/kbtu-mood-midterm-team2](https://github.com/Tasik1/kbtu-mood-midterm-team2)

### Team Members
- **Bidaishiev Shyntas (25MD0291)** — Team Lead, ETL & DFG Engineering, Git Repository Architect
- **Ibragim Anzir (25MD0311)** — AI Architect, GraphCodeBERT Integration, Graph Attention Layer
- **Ardak Aruzhan (25MD0308)** — Data Governance, Quality Assessment (DAMA/ISO), Ethics & Policy
- **Amanbayev Farkhad (25MD0304)** — Alternative Baseline (Frozen+RF), Visualizations & Strategic Analysis""")

    # Cell 2: Section 1
    add_md("""## 1. Environment Setup & Dependency Verification
In this step, we verify PyTorch, Transformers, Scikit-Learn, and hardware availability.""")

    add_code("""import os
import sys
sys.path.insert(0, os.path.abspath(".."))

import torch
import transformers
import sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

print(f"PyTorch Version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"Transformers Version: {transformers.__version__}")
print(f"Scikit-Learn Version: {sklearn.__version__}")""")

    # Cell 3: Lecture 1 & 4 ETL
    add_md("""## 2. Lecture 1 & 4 — Organizational Data Lifecycle & ETL Pipeline
We execute data extraction, validation, cleaning, and storage conforming to DAMA-DMBOK principles.""")

    add_code("""from pipeline.etl_pipeline import JavaVulnerabilityETL

etl = JavaVulnerabilityETL(
    raw_dir="../data/extracted",
    processed_dir="../data/processed"
)
quality_metrics = etl.run_etl()

print("ETL Completed. Data Quality Summary:")
print(json.dumps(quality_metrics["splits"], indent=2))""")

    # Cell 4: Lecture 5 Quality
    add_md("""## 3. Lecture 5 — Data Quality Assessment (ISO/IEC 25012)
We visualize class distributions, top Common Weakness Enumerations (CWE), and token lengths.""")

    add_code("""# Load cleaned data
with open("../data/processed/train_cleaned.jsonl", "r", encoding="utf-8") as f:
    train_data = [json.loads(l) for l in f]

df_train = pd.DataFrame(train_data)
print(f"Total Training Samples: {len(df_train)}")
print("Class Distribution:")
print(df_train["target"].value_counts(normalize=True))

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
sns.countplot(data=df_train, x="target", palette=["#2ca02c", "#d62728"])
plt.title("Class Balance (0: Non-Vuln, 1: Vuln)")
plt.xlabel("Target Label")

plt.subplot(1, 2, 2)
df_train["cwe"].value_counts().head(8).plot(kind="barh", color="#1f77b4")
plt.title("Top 8 CWE Categories in Training Set")
plt.xlabel("Frequency")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()""")

    # Cell 5: Data Flow Extraction
    add_md("""## 4. Data Flow Graph (DFG) Extraction for Java Code
We demonstrate the extraction of variable nodes, def-use chains, and adjacency matrices from Java methods.""")

    add_code("""from models.data_flow_extractor import JavaDataFlowExtractor

extractor = JavaDataFlowExtractor(max_dfg_nodes=16)

sample_code = \"\"\"
public byte[] processPayload(byte[] rawInput, boolean isEncrypted) {
    byte[] buffer = rawInput;
    if (isEncrypted) {
        buffer = decryptPayload(buffer);
    }
    return buffer;
}
\"\"\"

dfg_result = extractor.extract_variables_and_dfg(sample_code)

print("Java Code Tokens:", dfg_result["tokens"])
print("\\nExtracted DFG Variables (Nodes):", dfg_result["dfg_nodes"])
print("Def-Use Edges:", dfg_result["dfg_edges"])
print("Adjacency Matrix Shape:", dfg_result["adjacency_matrix"].shape)

# Visualize Adjacency Matrix
plt.figure(figsize=(5, 4))
sns.heatmap(dfg_result["adjacency_matrix"], annot=True, cbar=False, cmap="Blues",
            xticklabels=dfg_result["dfg_nodes"], yticklabels=dfg_result["dfg_nodes"])
plt.title("Variable Def-Use Adjacency Matrix A")
plt.show()""")

    # Cell 6: Models
    add_md("""## 5. Model Architectures
- **Primary Method**: GraphCodeBERT + Data Flow Classifier (Adjacency-guided Graph Attention)
- **Alternative Method**: GraphCodeBERT + Frozen Embeddings + Random Forest""")

    add_code("""from models.graphcodebert_classifier import GraphCodeBERTDataFlowClassifier
from models.alternative_classifier import GraphCodeBERTRandomForest

print("Primary Model Class:", GraphCodeBERTDataFlowClassifier.__name__)
print("Alternative Model Class:", GraphCodeBERTRandomForest.__name__)""")

    # Cell 7: Results
    add_md("""## 6. Experimental Results & Verification
We load the evaluation metrics, verify that **Accuracy >= 93%**, and plot the comparison.""")

    add_code("""with open("../results/metrics_summary.json", "r", encoding="utf-8") as f:
    results = json.load(f)

print("Team:", results["team"])
print("Topic:", results["topic"])
print("\\nPrimary Method Metrics:")
for k, v in results["primary_method"].items():
    if k not in ("true_labels", "predictions", "probabilities"):
        print(f"  {k}: {v}")

print("\\nAlternative Method Metrics:")
for k, v in results["alternative_method"].items():
    if k not in ("true_labels", "predictions", "probabilities"):
        print(f"  {k}: {v}")

print(f"\\nRequirement (Accuracy >= 93%): {results['comparison_summary']['primary_meets_93_threshold']}")""")

    # Cell 8: Plots
    add_md("""## 7. Visual Evidence & Analytics
Displaying publication-quality visualizations generated by the pipeline.""")

    add_code("""from IPython.display import Image, display

plots = [
    ("../results/confusion_matrix_primary.png", "Primary Model Confusion Matrix"),
    ("../results/confusion_matrix_alternative.png", "Alternative Model Confusion Matrix"),
    ("../results/roc_curve_comparison.png", "ROC Curves Comparison"),
    ("../results/metrics_barchart.png", "Evaluation Metrics Bar Chart"),
    ("../results/data_lifecycle_diagram.png", "Organizational Data Lifecycle"),
    ("../results/architecture_diagram.png", "System Architecture")
]

for path, title in plots:
    if os.path.exists(path):
        print(f"=== {title} ===")
        display(Image(filename=path))""")

    # Cell 9: Conclusion
    add_md("""## 8. Strategic Recommendations & Defense Conclusion
1. **Tiered Enterprise Architecture**: Deploy the fast Random Forest model for pre-commit developer IDE linting (<30ms latency), and route candidate suspicious functions to the primary GraphCodeBERT + DFG classifier for pull request gating.
2. **Data Governance & Continuous Quality**: Maintain ISO/IEC 25012 compliance with automated verification of commit hash integrity and de-identification of sensitive author credentials.
3. **Reproducibility**: The entire pipeline is open-source and hosted at `https://github.com/Tasik1/kbtu-mood-midterm-team2`.""")

    out_file = "midterm/notebooks/midterm_team2_graphcodebert.ipynb"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"[Notebook] Successfully generated {out_file}")

if __name__ == "__main__":
    create_notebook()
