"""
Script to package the Required Submission Package for KBTU MoOD 2026 Midterm Group Project.
Team 2: Bidaishiev S., Ibragim A., Ardak A., Amanbayev F.
Topic: GraphCodeBERT + Data Flow Classifier
"""

import os
import sys
import zipfile
import json
import hashlib

def get_file_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def build_package(
    source_dir: str = "midterm",
    output_zip_path: str = "Team2_Required_Submission_Package.zip"
):
    print("="*70)
    print("BUILDING REQUIRED SUBMISSION PACKAGE (TEAM 2)")
    print(f"Source Directory: {source_dir}")
    print(f"Output ZIP:       {output_zip_path}")
    print("="*70)

    # 1. Verify metrics and requirements
    metrics_path = os.path.join(source_dir, "results", "metrics_summary.json")
    if not os.path.exists(metrics_path):
        raise FileNotFoundError(f"Missing metrics summary at {metrics_path}")
    
    with open(metrics_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    
    acc = meta["evaluation_metrics"]["accuracy"]
    if acc < 0.93:
        raise ValueError(f"Accuracy {acc*100:.2f}% does not meet course threshold >= 93%!")
    print(f"[Check] Accuracy verified: {acc*100:.2f}% >= 93.0% (PASSED)")

    # 2. Files to include
    include_patterns = [
        # Root files
        "README.md",
        "requirements.txt",
        "run_all.py",
        "MoOD_10_Groups_Midterm_2026.docx",
        # Documentation
        "docs/Midterm_Report_Team2_Final.docx",
        "docs/Midterm_Report_Team2.docx",
        "docs/Midterm_Report_Team2.md",
        "docs/Midterm_Presentation_Team2.pptx",
        "docs/Laboratory Work Report Template.docx",
        "docs/generate_template_report.py",
        "docs/generate_presentation.py",
        # Notebooks
        "notebooks/midterm_team2_graphcodebert.ipynb",
        "notebooks/generate_notebook.py",
        # Pipeline
        "pipeline/etl_pipeline.py",
        "pipeline/train_eval.py",
        "pipeline/github_proxy.py",
        # Models
        "models/data_flow_extractor.py",
        "models/graphcodebert_classifier.py",
        "models/graphcodebert_dfg_model.pt",
        # Results & Visual Evidence
        "results/metrics_summary.json",
        "results/data_quality_report.json",
        "results/architecture_diagram.png",
        "results/data_lifecycle_diagram.png",
        "results/confusion_matrix.png",
        "results/roc_curve.png",
        "results/metrics_barchart.png",
        "results/screenshot_error_git_network.png",
        "results/screenshot_error_cuda_oom.png",
        "results/screenshot_git_push.png",
        # Data
        "data/java_k_1_strict_2023_07_03.tar.gz",
        "data/processed/train_cleaned.jsonl",
        "data/processed/valid_cleaned.jsonl",
        "data/processed/test_cleaned.jsonl"
    ]

    # Create submission checklist inside package
    checklist_content = f"""# KBTU MSITM 5134 MoOD 2026 — Midterm Submission Package Checklist
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
   - `docs/Midterm_Report_Team2_Final.docx`: Word report formatted strictly per Laboratory Work Report Template.
   - `docs/Midterm_Report_Team2.docx`: Word report copy.
   - `docs/Midterm_Report_Team2.md`: Full Markdown technical report.
   - Covers all 7 lecture topics, methodology, problems encountered, screenshots, results, and references.

3. **Presentation & Defense**:
   - `docs/Midterm_Presentation_Team2.pptx`: 9-slide defense deck with embedded figures, tables, and roles.

4. **Experimental Results & Visual Evidence**:
   - `results/metrics_summary.json`: Test Accuracy = {meta['evaluation_metrics']['accuracy']*100:.2f}% (>= 93% target met).
   - `results/data_quality_report.json`: ISO 25012 data quality scores (100% across all dimensions).
   - `results/architecture_diagram.png`: System architecture.
   - `results/data_lifecycle_diagram.png`: 7-stage DAMA-DMBOK data lifecycle.
   - `results/confusion_matrix.png`: Test set confusion matrix (TN=124, FP=5, FN=9, TP=114).
   - `results/roc_curve.png`: ROC curve (AUC = {meta['evaluation_metrics']['roc_auc']:.4f}).
   - `results/metrics_barchart.png`: Evaluation metrics bar chart.
   - `results/screenshot_error_git_network.png`: Network port 443 timeout & proxy fix evidence.
   - `results/screenshot_error_cuda_oom.png`: CUDA OutOfMemoryError & memory optimization evidence.
   - `results/screenshot_git_push.png`: Git push verification evidence under Tasik1.
"""
    checklist_temp_path = os.path.join(source_dir, "SUBMISSION_CHECKLIST.md")
    with open(checklist_temp_path, "w", encoding="utf-8") as f:
        f.write(checklist_content)

    include_patterns.append("SUBMISSION_CHECKLIST.md")

    manifest = []
    prefix = "Team2_Submission_Package"

    with zipfile.ZipFile(output_zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for rel_path in include_patterns:
            full_path = os.path.join(source_dir, rel_path)
            if not os.path.exists(full_path):
                print(f"[Warning] File not found: {full_path}")
                continue
            arcname = os.path.join(prefix, rel_path).replace("\\", "/")
            zf.write(full_path, arcname=arcname)
            file_size = os.path.getsize(full_path)
            manifest.append({
                "path": arcname,
                "size_bytes": file_size,
                "sha256": get_file_sha256(full_path)
            })
            print(f"  + Added: {arcname} ({file_size/1024:.1f} KB)")

    # Also make a copy directly inside midterm/ for convenience
    copy_in_midterm = os.path.join(source_dir, "Required_Submission_Package_Team2.zip")
    with open(output_zip_path, "rb") as src_f, open(copy_in_midterm, "wb") as dst_f:
        dst_f.write(src_f.read())

    print("\n" + "="*70)
    zip_size = os.path.getsize(output_zip_path)
    print(f"SUCCESS: Package built successfully!")
    print(f"Primary Output: {os.path.abspath(output_zip_path)} ({zip_size / (1024*1024):.2f} MB)")
    print(f"Midterm Copy:   {os.path.abspath(copy_in_midterm)} ({zip_size / (1024*1024):.2f} MB)")
    print(f"Total Files:    {len(manifest)}")
    print("="*70)

if __name__ == "__main__":
    build_package()
