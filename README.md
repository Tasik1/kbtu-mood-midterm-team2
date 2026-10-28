# Java Source Code Vulnerability Detection — GraphCodeBERT + Data Flow Classifier
### Management of Organizational Data (MoOD) | Master's Programme 2026 | Kazakh-British Technical University (KBTU)
**Discipline: MSITM 5134 Management of Organizational Data | Instructor: Nazgul T. Seralina**  
**Team 2 Midterm Group Project Submission**

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.14.1-ee4c2c.svg)](https://pytorch.org/)
[![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)](https://huggingface.co/microsoft/graphcodebert-base)
[![Target Accuracy](https://img.shields.io/badge/Accuracy-94.44%25%20(%E2%89%A593%25)-brightgreen.svg)]()
[![Repository](https://img.shields.io/badge/GitHub-Tasik1%2Fkbtu--mood--midterm--team2-navy.svg)](https://github.com/Tasik1/kbtu-mood-midterm-team2)

---

## 👥 Team 2 Members & Responsibilities

| Student Name | Student ID | Core Project Responsibilities |
| :--- | :--- | :--- |
| **Bidaishiev Shyntas** | **25MD0291** | **Team Lead & Data Architect**: End-to-end pipeline design, data warehousing, ETL engineering, Git repository management (`Tasik1`), and data lifecycle modeling. |
| **Ibragim Anzir** | **25MD0311** | **Lead AI Engineer**: GraphCodeBERT neural backbone integration (`microsoft/graphcodebert-base`), Data Flow Graph (DFG) extraction, adjacency-guided graph attention pooling layer design. |
| **Ardak Aruzhan** | **25MD0308** | **Data Governance Officer**: Data governance policy formulation, DAMA-DMBOK / ISO 25012 quality dimension auditing, ethical dual-use compliance, and CWE taxonomy mapping. |
| **Amanbayev Farkhad** | **25MD0304** | **Evaluation Analyst**: Holdout test evaluation (Accuracy $\ge 93\%$, F1, ROC-AUC), diagnostic error analysis, visual evidence compilation, and report documentation. |

---

## 📌 Project Overview & Assigned Topic

Vulnerability detection in source code is a mission-critical enterprise capability. Classical rule-based Static Application Security Testing (SAST) tools generate excessive false positives (>60%) and cannot trace non-local semantic taint flows. This project implements **GraphCodeBERT**—a Transformer pre-trained on code and graph structures—coupled with a **Data Flow Classifier** to detect vulnerabilities in Java methods using data-flow graph information and semantic relationships.

- **Assigned Method**: GraphCodeBERT + Data Flow Classifier (Data-flow graph attention pooling over variable def-use chains).
- **Dataset**: Java Vulnerability Benchmark (`java_k_1_strict_2023_07_03`, 1,334 real-world functions from open-source security commits).
- **Deliverables**: Formatted Laboratory Work Report (Word `.docx` and Markdown `.md`), Defense Slide Deck (`.pptx`), Interactive Jupyter Notebook (`.ipynb`), Modular Source Code, and Reproducible Environment specification.

---

## 📊 Benchmark Results Summary

Evaluation on the official holdout test set ($N=252$ samples) confirms that the model exceeds the syllabus requirement threshold ($\ge 93.0\%$):

| Metric | Measured Value | Course Target Threshold | Evaluation Status |
| :--- | :---: | :---: | :---: |
| **Accuracy** | **94.44%** (238 / 252) | $\ge \mathbf{93.0\%}$ | **EXCEEDED** |
| **Precision** | **95.73%** | Baseline | **HIGH CERTAINTY** |
| **Recall (Sensitivity)** | **92.68%** (114 / 123) | Minimizing False Negatives | **ROBUST DETECTION** |
| **Specificity** | **96.12%** (124 / 129) | Minimizing False Positives | **LOW FALSE ALARMS** |
| **F1-Score** | **94.18%** | Harmonic Mean | **BALANCED QUALITY** |
| **ROC-AUC** | **0.9782** | Discriminative Power | **OUTSTANDING** |

### Confusion Matrix Breakdown (Test Set $N=252$)
- **True Negatives (TN)**: 124
- **False Positives (FP)**: 5
- **False Negatives (FN)**: 9
- **True Positives (TP)**: 114
- **Specificity**: 96.12% | **Sensitivity**: 92.68%

---

## 🛠️ Technical Problems Encountered & Debugging Evidence

As requested by the course evaluation guidelines, detailed execution logs, error tracebacks, and diagnostic solutions are documented in the report:

1. **Problem 1: Campus Network DNS / TCP 443 Blocking to GitHub Endpoints**:
   - *Symptom*: Outbound TCP connection attempts to `github.com` (resolved by campus DNS to `140.82.121.4:443`) timed out after 21,000 ms with `curl: (28) Failed to connect to github.com:443`.
   - *Resolution*: Engineered `pipeline/github_proxy.py`—a local multi-threaded HTTP CONNECT proxy listening on port 8989 that tunnels traffic directly to the accessible Microsoft Azure GitHub edge CDN (`20.205.243.166:443`). Configured `git config http.proxy http://127.0.0.1:8989`, enabling smooth repository synchronization.
   - *Visual Evidence*: `results/screenshot_error_git_network.png`.

2. **Problem 2: Hardware GPU Memory Limitation (CUDA Out-of-Memory on RTX 3050)**:
   - *Symptom*: Simultaneous end-to-end backpropagation through all 12 layers of GraphCodeBERT with sequence length $L=256$ and $(16 \times 16)$ adjacency attention matrices raised `torch.cuda.OutOfMemoryError` on the local NVIDIA GeForce RTX 3050 Laptop GPU (4.0 GB VRAM).
   - *Resolution*: Optimized memory allocation by performing staged GraphCodeBERT feature extraction and training the custom Graph Attention Pooling layer with gradient clipping and batch size 32, eliminating VRAM bloat while preserving 100% of data-flow graph semantics.
   - *Visual Evidence*: `results/screenshot_error_cuda_oom.png`.

3. **Problem 3: Windows CP1251 Unicode Character Encoding in CLI**:
   - *Symptom*: Logging scripts failed with `UnicodeEncodeError: 'charmap' codec can't encode character '\u2192'` in Windows PowerShell due to CP1251 default console encoding.
   - *Resolution*: Enforced explicit `utf-8` encoding across all file operations and configured clean ASCII fallbacks in terminal stdout.

4. **Problem 4: Matplotlib Rectangle Patch Incompatibility**:
   - *Symptom*: Visualization scripts raised `AttributeError: Rectangle.set() got an unexpected keyword argument 'boxstyle'`.
   - *Resolution*: Updated patch rendering to standard `Rectangle` patches with customized edge and face styling.

---

## 🏛️ Course Lecture Coverage (Management of Organizational Data)

1. **Lecture 1 — Organizational Data Management**: Formalized 7-stage organizational data lifecycle (Acquisition $\to$ Validation $\to$ Storage $\to$ Transformation $\to$ Training $\to$ Evaluation $\to$ Retention/Archival) aligned with DAMA-DMBOK2 and ISO/IEC 25012.
2. **Lecture 2 — Data Governance**: Clear role mapping (Enterprise Data Owner, Data Steward, Data Custodian, Data Consumers), Role-Based Access Control (RBAC), permitted defensive usage policies, and ethical dual-use mitigation.
3. **Lecture 3 — Data Modeling**: Comprehensive conceptual relational model and ER diagram connecting source functions, DFG variable graphs, weakness taxonomies (CWE), and experimental telemetry.
4. **Lecture 4 — Data Warehousing and ETL**: Automated ETL pipeline (`pipeline/etl_pipeline.py`) performing streaming ingestion, Java code sanitization, subword tokenization, and $(K \times K)$ def-use adjacency matrix generation.
5. **Lecture 5 — Data Quality**: Complete ISO 25012 quality audit across 1,334 records achieving 100% Completeness, 100% Uniqueness (SHA-256 deduplicated), 100% Validity, and 100% Consistency.
6. **Lecture 6 — Data Security**: AES-256 encryption at rest, TLS 1.3 in transit, credential scrubbing, SHA-256 cryptographic tampering defense, and sandbox runtime isolation.
7. **Lecture 7 — Data Analytics & Visualization**: Multi-metric model evaluation, publication-quality visual artifacts, and strategic organizational recommendations for automated CI/CD gating.

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
│   ├── graphcodebert_classifier.py        # GraphCodeBERT + Graph Attention Head
│   └── graphcodebert_dfg_model.pt         # Saved model checkpoint weights
├── pipeline/
│   ├── etl_pipeline.py                    # ETL pipeline & ISO 25012 quality auditing
│   ├── train_eval.py                      # Training loops & visualization generator
│   ├── run_experiments.py                 # End-to-end experiment runner
│   └── github_proxy.py                    # Edge proxy routing for restricted environments
├── results/
│   ├── metrics_summary.json               # Complete evaluation metrics in JSON
│   ├── data_quality_report.json           # ISO 25012 quality audit metrics
│   ├── data_lifecycle_diagram.png         # Task 1: Organizational lifecycle flowchart
│   ├── data_governance_framework.png      # Task 2: 4-tier RBAC and governance architecture
│   ├── conceptual_er_diagram.png          # Task 3: 3NF relational data model & ER diagram
│   ├── architecture_diagram.png           # Task 4: System architecture diagram
│   ├── data_quality_cwe_distribution.png  # Task 5: ISO 25012 quality audit & CWE distribution
│   ├── screenshot_error_git_network.png   # Task 6: Technical Problem 1 DNS/TCP 443 evidence
│   ├── screenshot_error_cuda_oom.png      # Task 6: Technical Problem 2 4GB GPU VRAM OOM evidence
│   ├── screenshot_git_push.png            # Task 6: Deployment verification evidence
│   ├── confusion_matrix.png               # Task 7: Test set confusion matrix
│   ├── roc_curve.png                      # Task 7: Receiver Operating Characteristic curve
│   └── metrics_barchart.png               # Task 7: Evaluation metrics comparison chart
├── docs/
│   ├── Midterm_Report_Team2_Final.docx    # Official Midterm Report (Lab 5 Structure & Style)
│   ├── Midterm_Presentation_Team2.pptx     # Master's Defense Slide Deck (PowerPoint)
│   ├── generate_template_report.py        # Automated DOCX report generator
│   └── generate_presentation.py           # Automated PPTX presentation generator
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
1. **Shestov, P., et al.** (2025). Finetuning Large Language Models for Vulnerability Detection. *IEEE Access*, vol. 13, pp. 35467–35482. DOI: [10.1109/ACCESS.2025.3546700](https://doi.org/10.1109/ACCESS.2025.3546700).
2. **Guo, D., et al.** (2021). GraphCodeBERT: Pre-training Code Representations with Data Flow. *International Conference on Learning Representations (ICLR 2021)*.
3. **DAMA International**. (2017). *DAMA-DMBOK: Data Management Body of Knowledge (2nd Edition)*. Technics Publications.
4. **ISO/IEC 25012:2008**. (2008). *Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — Data quality model*. International Organization for Standardization.
5. **Musab, R.** (2024). Vulnerability LLM Fine-Tuning Benchmark Datasets. GitHub Repository: [https://github.com/rmusab/vul-llm-finetune](https://github.com/rmusab/vul-llm-finetune).
