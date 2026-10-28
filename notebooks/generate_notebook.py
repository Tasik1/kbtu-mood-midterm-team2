"""
Generates the comprehensive Jupyter Notebook for Team 2 Midterm.
Course: MSITM 5134 Management of Organizational Data (MoOD) 2026 - Master's Programme
Team 2: Bidaishiev Shyntas, Ibragim Anzir, Ardak Aruzhan, Amanbayev Farkhad
Topic: Java Source Code Vulnerability Detection (GraphCodeBERT + Data Flow Classifier)
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
## Master's Programme — MSITM 5134 Management of Organizational Data (MoOD) 2026
### Midterm Group Project: Java Source Code Vulnerability Detection
---
**Team**: Group 2  
**Assigned Method**: GraphCodeBERT + Data Flow Classifier  
**Instructor**: Nazgul T. Seralina  
**Repository**: [https://github.com/Tasik1/kbtu-mood-midterm-team2](https://github.com/Tasik1/kbtu-mood-midterm-team2)

### Team Members & Roles
- **Bidaishiev Shyntas (25MD0291)** — Team Lead, ETL & DFG Engineering, Git Repository Architect
- **Ibragim Anzir (25MD0311)** — Lead AI Engineer, GraphCodeBERT Implementation, Graph Attention Layer
- **Ardak Aruzhan (25MD0308)** — Data Governance, Quality Assessment (DAMA/ISO), Ethics & Policy
- **Amanbayev Farkhad (25MD0304)** — Evaluation Analyst, Visual Evidence & Report Documentation""")

    # Cell 2: Section 1
    add_md("""## 1. Environment Setup & Dependency Verification
Verify PyTorch, Transformers, Scikit-Learn, and hardware availability.""")

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
Execute data extraction, validation, cleaning, and storage conforming to DAMA-DMBOK principles.""")

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
Visualize class distributions, top Common Weakness Enumerations (CWE), and token lengths.""")

    add_code("""with open("../data/processed/train_cleaned.jsonl", "r", encoding="utf-8") as f:
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
Extract variable nodes, def-use chains, and adjacency matrices from Java methods.""")

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

plt.figure(figsize=(5, 4))
sns.heatmap(dfg_result["adjacency_matrix"], annot=True, cbar=False, cmap="Blues",
            xticklabels=dfg_result["dfg_nodes"], yticklabels=dfg_result["dfg_nodes"])
plt.title("Variable Def-Use Adjacency Matrix A")
plt.show()""")

    # Cell 6: Model Architecture
    add_md("""## 5. Model Architecture: GraphCodeBERT + Data Flow Classifier
Graph attention pooling layer refining variable nodes guided by def-use adjacency matrix $A$.""")

    add_code("""from models.graphcodebert_classifier import GraphCodeBERTDataFlowClassifier

model = GraphCodeBERTDataFlowClassifier(
    model_name="microsoft/graphcodebert-base",
    num_classes=2,
    dropout_prob=0.2
)
print("Initialized Model Architecture:")
print(model)""")

    # Cell 7: Results
    add_md("""## 6. Experimental Results & Verification
Loading evaluation metrics and verifying that **Accuracy >= 93%**.""")

    add_code("""with open("../results/metrics_summary.json", "r", encoding="utf-8") as f:
    results = json.load(f)

print("Team:", results["team"])
print("Topic:", results["topic"])
print("Assigned Method:", results["assigned_method"])
print("\\nEvaluation Metrics:")
for k, v in results["evaluation_metrics"].items():
    print(f"  {k}: {v}")

print(f"\\nRequirement Met (Accuracy >= 93%): {results['requirements_compliance']['accuracy_ge_93_threshold']}")""")

    # Cell 8: Plots
    add_md("""## 7. Visual Evidence & Analytics
Visualizations generated by the pipeline.""")

    add_code("""from IPython.display import Image, display

plots = [
    ("../results/confusion_matrix.png", "Confusion Matrix"),
    ("../results/roc_curve.png", "ROC Curve"),
    ("../results/metrics_barchart.png", "Evaluation Metrics Bar Chart"),
    ("../results/architecture_diagram.png", "System Architecture Diagram"),
    ("../results/data_lifecycle_diagram.png", "Organizational Data Lifecycle Flowchart"),
    ("../results/screenshot_error_git_network.png", "Technical Problem 1: Campus Network DNS / TCP 443 Resolution"),
    ("../results/screenshot_error_cuda_oom.png", "Technical Problem 2: 4GB GPU VRAM Memory Constraint & Fix")
]

for path, title in plots:
    if os.path.exists(path):
        print(f"=== {title} ===")
        display(Image(filename=path))""")

    # Cell 9: Conclusion
    add_md("""## 8. Strategic Recommendations & Defense Conclusion
1. **Automated CI/CD Gating**: Deploy the GraphCodeBERT + Data Flow Classifier as a mandatory merge check blocking vulnerable Java pull requests.
2. **Continuous Data Governance**: Implement feedback loops where security triage findings update the training dataset, maintaining ISO/IEC 25012 data quality standards.
3. **Reproducibility**: All code, data, diagrams, reports, presentation slides, and environment files are available at [https://github.com/Tasik1/kbtu-mood-midterm-team2](https://github.com/Tasik1/kbtu-mood-midterm-team2).""")

    out_file = "midterm/notebooks/midterm_team2_graphcodebert.ipynb"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"[Notebook] Successfully generated {out_file}")

if __name__ == "__main__":
    create_notebook()
