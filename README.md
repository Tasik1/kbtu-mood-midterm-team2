# Java Source Code Vulnerability Detection — GraphCodeBERT + Data Flow Classifier
### Management of Organizational Data (MoOD) | Master's Programme 2026 | Kazakh-British Technical University (KBTU)
**Team 2 Group Project Submission**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg)](https://pytorch.org/)
[![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)](https://huggingface.co/microsoft/graphcodebert-base)
[![Target Accuracy](https://img.shields.io/badge/Accuracy-94.44%25%20(%E2%89%A593%25)-brightgreen.svg)]()
[![Repository](https://img.shields.io/badge/GitHub-Tasik1%2Fkbtu--mood--midterm--team2-navy.svg)](https://github.com/Tasik1/kbtu-mood-midterm-team2)

---

## 👥 Team 2 Members & Responsibilities

| Student Name | Student ID | Core Project Responsibilities |
| :--- | :--- | :--- |
| **Bidaishiev Shyntas** | **25MD0291** | **Team Lead & Data Architect**: End-to-end pipeline design, data warehousing, ETL engineering, Git repository management, and data lifecycle modeling. |
| **Ibragim Anzir** | **25MD0311** | **Lead AI Engineer**: GraphCodeBERT neural backbone integration, Data Flow Graph (DFG) extraction, adjacency-guided graph attention pooling layer design. |
| **Ardak Aruzhan** | **25MD0308** | **Data Governance Officer**: Data governance policy formulation, DAMA-DMBOK/ISO 25012 quality dimension auditing, ethical and legal compliance. |
| **Amanbayev Farkhad** | **25MD0304** | **ML Systems & Evaluation Analyst**: Alternative model (Frozen Embeddings + Random Forest) implementation, hyperparameter optimization, ROC/confusion matrix analytics, and report authoring. |

---

## 📌 Project Overview & Assigned Topic

Vulnerability detection in source code is a mission-critical enterprise capability. Classical rule-based Static Application Security Testing (SAST) tools generate excessive false positives (>60%) and cannot trace non-local semantic taint flows. This project leverages **GraphCodeBERT**—a Transformer pre-trained on code and graph structures—coupled with a **Data Flow Classifier** to detect vulnerabilities in Java methods.

- **Primary Method**: GraphCodeBERT + Data Flow Classifier (Data-flow graph attention pooling over variable def-use chains).
- **Alternative Method**: GraphCodeBERT + Frozen Embeddings + Random Forest (Evaluated under syllabus guidelines for edge/resource-constrained environments).
- **Dataset**: Java Vulnerability Benchmark (`java_k_1_strict_2023_07_03`, 1,334 real-world functions from open-source security commits).

---

## 📊 Benchmark Results Summary

Evaluation on the official holdout test set ($N=252$ samples) confirms that the primary model exceeds the course threshold ($\ge 93\%$):

| Metric | Primary: GraphCodeBERT + DFG Classifier | Alternative: Frozen Embeddings + Random Forest | Delta ($\Delta$) | Course Target Threshold |
| :--- | :---: | :---: | :---: | :---: |
| **Accuracy** | **94.44%** | **88.49%** | **+5.95%** | $\ge \mathbf{93.0\%}$ (Exceeded) |
| **Precision** | **95.73%** | **89.83%** | **+5.90%** | Baseline |
| **Recall (Sensitivity)** | **92.68%** | **86.18%** | **+6.50%** | Minimizing False Negatives |
| **F1-Score** | **94.18%** | **87.97%** | **+6.21%** | Balanced Quality |
| **ROC-AUC** | **0.9782** | **0.9486** | **+0.0296** | Discriminative Power |

### Confusion Matrix Breakdown (Test Set $N=252$)
- **Primary Method**: True Negatives (TN): 124 | False Positives (FP): 5 | False Negatives (FN): 9 | True Positives (TP): 114
  - **Specificity**: 96.12% | **Sensitivity**: 92.68%
- **Alternative Method**: True Negatives (TN): 117 | False Positives (FP): 12 | False Negatives (FN): 17 | True Positives (TP): 106

---

## 🏛️ Course Lecture Coverage (Management of Organizational Data)

1. **Lecture 1 — Organizational Data Management**: Formalized 7-stage organizational data lifecycle (Acquisition $\to$ Validation $\to$ Storage $\to$ Transformation $\to$ Training $\to$ Evaluation $\to$ Retention/Archival) aligned with DAMA-DMBOK2 and ISO/IEC 25012.
2. **Lecture 2 — Data Governance**: Clear role mapping (Enterprise Data Owner, Data Steward, Data Custodian, Data Consumers), Role-Based Access Control (RBAC), permitted defensive usage policies, and ethical dual-use mitigation.
3. **Lecture 3 — Data Modeling**: Comprehensive conceptual relational model and ER diagram connecting source functions, DFG variable graphs, weakness taxonomies (CWE), and experimental telemetry.
4. **Lecture 4 — Data Warehousing and ETL**: Automated ETL pipeline (`pipeline/etl_pipeline.py`) performing streaming ingestion, Java code sanitization, subword tokenization, and $(K \times K)$ def-use adjacency matrix generation.
5. **Lecture 5 — Data Quality**: Complete ISO 25012 quality audit across 1,334 records achieving 100% Completeness, 100% Uniqueness (SHA-256 deduplicated), 100% Validity, and 100% Consistency.
6. **Lecture 6 — Data Security**: AES-256 encryption at rest, TLS 1.3 in transit, credential scrubbing, SHA-256 cryptographic tampering defense, and sandbox runtime isolation.
7. **Lecture 7 — Data Analytics & Visualization**: Multi-metric model evaluation, 6 publication-quality visual artifacts, and strategic organizational recommendations for tiered DevSecOps deployment.

---

## 🖼️ Visual Evidence & Architecture

All visualizations are generated and saved in `results/`:
- `results/architecture_diagram.png` — System architecture diagram.
- `results/data_lifecycle_diagram.png` — DAMA-DMBOK aligned 7-stage data lifecycle.
- `results/confusion_matrix_primary.png` — Confusion matrix for GraphCodeBERT + DFG Classifier.
- `results/confusion_matrix_alternative.png` — Confusion matrix for Random Forest Alternative.
- `results/roc_curve_comparison.png` — Receiver Operating Characteristic (ROC) curve comparison.
- `results/metrics_barchart.png` — Performance comparison bar chart against the 93% requirement threshold.

---

## 📁 Repository Directory Structure

```
kbtu-mood-midterm-team2/
├── data/
│   ├── java_k_1_strict_2023_07_03.tar.gz  # Raw compressed benchmark dataset
│   ├── extracted/                         # Extracted raw jsonl (train, valid, test)
│   └── processed/                         # Normalized, validated, deduplicated jsonl
├── models/
│   ├── data_flow_extractor.py             # Java variable & def-use graph extractor
│   ├── graphcodebert_classifier.py        # Primary: GraphCodeBERT + Graph Attention Head
│   └── alternative_classifier.py          # Alternative: Frozen Embeddings + Random Forest
├── pipeline/
│   ├── etl_pipeline.py                    # ETL pipeline & ISO 25012 quality auditing
│   ├── train_eval.py                      # Training loops & visualization generator
│   └── github_proxy.py                    # Edge proxy routing for restricted environments
├── results/
│   ├── metrics_summary.json               # Complete metrics & confusion matrices in JSON
│   ├── data_quality_report.json           # ISO 25012 quality audit metrics
│   ├── architecture_diagram.png           # System architecture diagram
│   ├── data_lifecycle_diagram.png         # Organizational lifecycle flowchart
│   ├── confusion_matrix_primary.png       # Primary model confusion matrix
│   ├── confusion_matrix_alternative.png   # Alternative model confusion matrix
│   ├── roc_curve_comparison.png           # ROC curves comparison
│   └── metrics_barchart.png               # Evaluation metrics comparison chart
├── docs/
│   ├── Midterm_Report_Team2.docx           # Master's Technical Report (Word)
│   ├── Midterm_Report_Team2.md             # Master's Technical Report (Markdown)
│   ├── Midterm_Presentation_Team2.pptx     # Master's Defense Slide Deck (PowerPoint)
│   ├── generate_docx_report.py            # Automated DOCX report compiler
│   └── generate_presentation.py           # Automated PPTX presentation compiler
├── notebooks/
│   ├── midterm_team2_graphcodebert.ipynb  # End-to-end runnable Jupyter Notebook
│   └── generate_notebook.py               # Notebook generator script
├── requirements.txt                       # Reproducible Python dependencies
├── run_all.py                             # One-click master reproducibility script
└── README.md                              # Main documentation and guide
```

---

## 🚀 Step-by-Step Reproduction Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Tasik1/kbtu-mood-midterm-team2.git
cd kbtu-mood-midterm-team2
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the Complete End-to-End Pipeline
Execute the master one-click runner to run ETL, generate reports, slides, and notebook:
```bash
python run_all.py
```

### 4. Interactive Jupyter Notebook
Launch the notebook to inspect the step-by-step data engineering and evaluation:
```bash
jupyter notebook notebooks/midterm_team2_graphcodebert.ipynb
```

---

## 📖 Scientific References
1. **Shestov et al.**, “Finetuning Large Language Models for Vulnerability Detection,” *IEEE Access*, vol. 13, 2025. DOI: [10.1109/ACCESS.2025.3546700](https://doi.org/10.1109/ACCESS.2025.3546700).
2. **Guo et al.**, “GraphCodeBERT: Pre-training Code Representations with Data Flow,” *International Conference on Learning Representations (ICLR)*, 2021.
3. **DAMA International**, *The DAMA Guide to the Data Management Body of Knowledge (DAMA-DMBOK2)*, Technics Publications, 2017.
4. **ISO/IEC 25012:2008**, *Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — Data quality model*, 2008.
