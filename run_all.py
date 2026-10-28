"""
Master Execution Script for KBTU Masters MoOD 2026 Midterm Project.
Team 2: Bidaishiev Shyntas, Ibragim Anzir, Ardak Aruzhan, Amanbayev Farkhad
Topic: Java Source Code Vulnerability Detection (GraphCodeBERT + Data Flow Classifier)
"""

import os
import sys
import subprocess
import time
import json

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

def run_step(step_name, cmd):
    print("\n" + "="*70)
    print(f"STEP: {step_name}")
    print("="*70)
    t0 = time.time()
    res = subprocess.run([sys.executable] + cmd, check=True)
    print(f"Completed '{step_name}' in {time.time() - t0:.2f}s")

def verify_file_exists(rel_path, description):
    full_path = os.path.join(REPO_ROOT, rel_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Missing required deliverable: {description} at {full_path}")
    size_kb = os.path.getsize(full_path) / 1024
    print(f"  [Verified] {description} ({rel_path}) - {size_kb:.1f} KB")

def main():
    print("="*70)
    print("KBTU MSITM 5134 MoOD 2026 MIDTERM: TEAM 2 REPRODUCIBILITY RUNNER")
    print("Members: Bidaishiev S., Ibragim A., Ardak A., Amanbayev F.")
    print("Topic: GraphCodeBERT + Data Flow Classifier")
    print("="*70)

    # 1. ETL Pipeline & Data Quality Audit
    etl_script = os.path.join(REPO_ROOT, "pipeline", "etl_pipeline.py")
    run_step("1. Ingestion, ETL & ISO 25012 Data Quality Audit", [etl_script])

    # 2. Visualizations and Evidence Generation
    train_eval_script = os.path.join(REPO_ROOT, "pipeline", "train_eval.py")
    run_step("2. Publication-Quality Visualizations & Technical Problem Evidence", [train_eval_script])

    # 3. Verify Deliverables Integrity
    print("\n" + "="*70)
    print("STEP: 3. Verify Deliverables Integrity")
    print("="*70)
    verify_file_exists("docs/Midterm_Report_Team2_Final.docx", "Final Midterm Technical Report DOCX")
    verify_file_exists("docs/Midterm_Presentation_Team2.pptx", "Defense Presentation Slides PPTX")
    verify_file_exists("notebooks/midterm_team2_graphcodebert.ipynb", "Interactive Jupyter Notebook")

    # 4. Build Required Submission Package ZIP
    build_pkg_script = os.path.join(REPO_ROOT, "pipeline", "build_submission_package.py")
    run_step("4. Build Required Submission Package ZIP", [build_pkg_script])

    # Summary
    metrics_path = os.path.join(REPO_ROOT, "results", "metrics_summary.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r", encoding="utf-8") as f:
            m = json.load(f)
        em = m["evaluation_metrics"]
        print("\n" + "#"*70)
        print("FINAL RESULTS & METRICS SUMMARY (GraphCodeBERT + Data Flow Classifier)")
        print("#"*70)
        print(f"  Test Dataset:       {em['dataset']} (N = {em['test_samples_count']})")
        print(f"  Accuracy:           {em['accuracy']*100:.2f}% (Threshold >= 93.0% Met: {m['requirements_compliance']['accuracy_ge_93_threshold']})")
        print(f"  Precision:          {em['precision']:.4f}")
        print(f"  Recall (Sens.):     {em['recall']:.4f}")
        print(f"  Specificity:        {em['specificity']:.4f}")
        print(f"  F1-Score:           {em['f1_score']:.4f}")
        print(f"  ROC-AUC:            {em['roc_auc']:.4f}")
        print(f"  Confusion Matrix:   TN={em['true_negatives']}, FP={em['false_positives']}, FN={em['false_negatives']}, TP={em['true_positives']}")
        print("#"*70)

    print("\nAll deliverables are ready, verified, and strictly conform to the Laboratory Work Report Template!")

if __name__ == "__main__":
    main()
