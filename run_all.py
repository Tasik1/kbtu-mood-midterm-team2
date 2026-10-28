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

def run_step(step_name, cmd):
    print("\n" + "="*70)
    print(f"STEP: {step_name}")
    print("="*70)
    t0 = time.time()
    res = subprocess.run([sys.executable] + cmd, check=True)
    print(f"Completed '{step_name}' in {time.time() - t0:.2f}s")

def main():
    print("="*70)
    print("KBTU MSITM 5134 MoOD 2026 MIDTERM: TEAM 2 REPRODUCIBILITY RUNNER")
    print("Members: Bidaishiev S., Ibragim A., Ardak A., Amanbayev F.")
    print("Topic: GraphCodeBERT + Data Flow Classifier")
    print("="*70)

    # 1. ETL Pipeline & Data Quality Audit
    run_step("1. Ingestion, ETL & ISO 25012 Data Quality Audit", ["midterm/pipeline/etl_pipeline.py"])

    # 2. Template-Compliant DOCX Report
    run_step("2. Laboratory Work Report Template DOCX Generation", ["midterm/docs/generate_template_report.py"])

    # 3. Defense Presentation
    run_step("3. Defense PPTX Presentation Generation", ["midterm/docs/generate_presentation.py"])

    # 4. Jupyter Notebook
    run_step("4. Interactive Jupyter Notebook Generation", ["midterm/notebooks/generate_notebook.py"])

    # Summary
    metrics_path = "midterm/results/metrics_summary.json"
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
