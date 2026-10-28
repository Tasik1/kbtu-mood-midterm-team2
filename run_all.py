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
    print("KBTU MoOD 2026 MIDTERM: TEAM 2 REPRODUCIBILITY RUNNER")
    print("Members: Bidaishiev S., Ibragim A., Ardak A., Amanbayev F.")
    print("Assigned: GraphCodeBERT + Data Flow Classifier")
    print("="*70)

    # 1. ETL Pipeline
    run_step("1. Ingestion, ETL & Data Quality Audit", ["midterm/pipeline/etl_pipeline.py"])

    # 2. DOCX Report
    run_step("2. Academic DOCX Report Generation", ["midterm/docs/generate_docx_report.py"])

    # 3. PPTX Presentation
    run_step("3. Defense PPTX Presentation Generation", ["midterm/docs/generate_presentation.py"])

    # 4. Jupyter Notebook
    run_step("4. Interactive Jupyter Notebook Generation", ["midterm/notebooks/generate_notebook.py"])

    # Summary
    metrics_path = "midterm/results/metrics_summary.json"
    if os.path.exists(metrics_path):
        with open(metrics_path, "r", encoding="utf-8") as f:
            m = json.load(f)
        print("\n" + "#"*70)
        print("FINAL RESULTS & METRICS SUMMARY")
        print("#"*70)
        print(f"Primary Method (GraphCodeBERT + DFG):")
        print(f"  Accuracy:  {m['primary_method']['accuracy']*100:.2f}% (Threshold >= 93% Met: {m['comparison_summary']['primary_meets_93_threshold']})")
        print(f"  Precision: {m['primary_method']['precision']:.4f}")
        print(f"  Recall:    {m['primary_method']['recall']:.4f}")
        print(f"  F1-Score:  {m['primary_method']['f1_score']:.4f}")
        print(f"  ROC-AUC:   {m['primary_method']['roc_auc']:.4f}")
        print(f"\nAlternative Method (Frozen Embeddings + Random Forest):")
        print(f"  Accuracy:  {m['alternative_method']['accuracy']*100:.2f}%")
        print(f"  Precision: {m['alternative_method']['precision']:.4f}")
        print(f"  Recall:    {m['alternative_method']['recall']:.4f}")
        print(f"  F1-Score:  {m['alternative_method']['f1_score']:.4f}")
        print(f"  ROC-AUC:   {m['alternative_method']['roc_auc']:.4f}")
        print("#"*70)

    print("\nAll deliverables are ready and verified!")

if __name__ == "__main__":
    main()
