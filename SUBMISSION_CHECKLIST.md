# KBTU MSITM 5134 MoOD 2026 — Midterm Submission Package Checklist
**Team**: Group 2  
**Assigned Method**: GraphCodeBERT + Data Flow Classifier  
**Instructor**: Nazgul T. Seralina  
**Repository**: https://github.com/Tasik1/kbtu-mood-midterm-team2  

---

## 1. Team Members & Contributions
- **Bidaishiev Shyntas (25MD0291)** — Team Lead, ETL & DFG Engineering, Git Repository Management
- **Ibragim Anzir (25MD0311)** — Lead AI Engineer, GraphCodeBERT Implementation, Graph Attention
- **Ardak Aruzhan (25MD0308)** — Data Governance, Quality Assessment (ISO 25012), Ethics & Policy
- **Amanbayev Farkhad (25MD0304)** — Evaluation Analyst, Visual Evidence & Report Documentation

---

## 2. Deliverables Mapping to Evaluation Rubric
1. **Source Code & Reproducibility**:
   - `models/data_flow_extractor.py`: AST lexer, variable tracking, def-use chains, adjacency matrix.
   - `models/graphcodebert_classifier.py`: 4-Head GAT layer, tri-fusion, deep classification head.
   - `pipeline/etl_pipeline.py`: Ingestion, cleaning, schema validation, ISO 25012 quality report.
   - `pipeline/train_eval.py`: Training loop, evaluation, and visual evidence generation.
   - `notebooks/midterm_team2_graphcodebert.ipynb`: Interactive Jupyter Notebook.
   - `requirements.txt` & `README.md`: Environment setup and run instructions.
   - `run_all.py`: Master one-click verification script.

2. **Technical Report**:
   - `docs/Midterm_Report_Team2_Final.docx`: Word report formatted strictly per Laboratory Work Report Template and Lab 5 structure.
   - Covers all 7 lecture topics, methodology, problems encountered, screenshots, results, and references.

3. **Presentation & Defense**:
   - `docs/Midterm_Presentation_Team2.pptx`: 9-slide defense deck with embedded figures, tables, and roles.

4. **Experimental Results & Visual Evidence**:
   - `results/metrics_summary.json`: Test Accuracy = 94.44% (>= 93% target met).
   - `results/data_quality_report.json`: ISO 25012 data quality scores (100% across all dimensions).
   - `results/architecture_diagram.png`: System architecture.
   - `results/data_lifecycle_diagram.png`: 7-stage DAMA-DMBOK data lifecycle.
   - `results/confusion_matrix.png`: Test set confusion matrix (TN=124, FP=5, FN=9, TP=114).
   - `results/roc_curve.png`: ROC curve (AUC = 0.9782).
   - `results/metrics_barchart.png`: Evaluation metrics bar chart.
   - `results/screenshot_error_git_network.png`: Network port 443 timeout & proxy fix evidence.
   - `results/screenshot_error_cuda_oom.png`: CUDA OutOfMemoryError & memory optimization evidence.
   - `results/screenshot_git_push.png`: Git push verification evidence under Tasik1.
