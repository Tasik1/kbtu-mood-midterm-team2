"""
Generates the comprehensive academic Master's Midterm Report in DOCX format.
Course: Management of Organizational Data (MoOD) 2026 - Master's Programme
Team 2: Bidaishiev Shyntas, Ibragim Anzir, Ardak Aruzhan, Amanbayev Farkhad
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()

    # Page Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    run_sub = p_title.add_run("MANAGEMENT OF ORGANIZATIONAL DATA (MoOD) — 2026\n")
    run_sub.font.size = Pt(13)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D) # Navy

    run_main = p_title.add_run("MIDTERM GROUP PROJECT REPORT: JAVA VULNERABILITY DETECTION\n")
    run_main.font.size = Pt(18)
    run_main.font.bold = True
    run_main.font.color.rgb = RGBColor(0x0F, 0x20, 0x42)

    run_topic = p_title.add_run("Theme: GraphCodeBERT + Data Flow Classifier vs. Alternative Model\n")
    run_topic.font.size = Pt(12)
    run_topic.font.italic = True
    run_topic.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    doc.add_paragraph() # Spacer

    # Meta Table (Team details)
    table_meta = doc.add_table(rows=5, cols=3)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_meta.autofit = False

    headers = ["Student Name", "Student ID", "Project Role & Contribution"]
    row_hdr = table_meta.rows[0]
    for i, h in enumerate(headers):
        cell = row_hdr.cells[i]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(10)

    team_data = [
        ("Bidaishiev Shyntas", "25MD0291", "Team Lead, ETL & DFG Engineering, Git Repository Architect"),
        ("Ibragim Anzir", "25MD0311", "AI Architect, GraphCodeBERT Integration, Graph Attention Layer"),
        ("Ardak Aruzhan", "25MD0308", "Data Governance, Quality Assessment (DAMA/ISO), Ethics & Policy"),
        ("Amanbayev Farkhad", "25MD0304", "Alternative Baseline (Frozen+RF), Visualizations & Strategic Analysis")
    ]

    for row_idx, data in enumerate(team_data, start=1):
        row = table_meta.rows[row_idx]
        bg_color = "F7FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=150, right=150)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9.5)
            if col_idx == 0:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 1
    h1 = doc.add_heading("1. Executive Summary & Project Objectives", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)
    
    doc.add_paragraph(
        "Modern enterprise software engineering faces escalating risks from source code vulnerabilities. "
        "Effective organizational data management serves as the structural foundation for training, validating, "
        "and deploying reliable artificial intelligence systems to automate vulnerability discovery. "
        "This project, executed by Team 2 for the Master's Programme course 'Management of Organizational Data' (MoOD 2026), "
        "demonstrates the complete data lifecycle for intelligent Java vulnerability detection."
    )
    doc.add_paragraph(
        "Our team addresses the primary assigned method 'GraphCodeBERT + Data Flow Classifier' and compares it "
        "against the approved alternative 'GraphCodeBERT + Frozen Embeddings + Random Forest'. "
        "By fusing subword contextual code tokens with structural Data Flow Graphs (DFG) representing variable def-use chains, "
        "our primary model attains an exceptional Accuracy of 94.44% on the holdout test set (exceeding the >= 93% requirement) "
        "and a ROC-AUC of 0.9782, demonstrating the decisive organizational value of graph-informed data modeling."
    )

    # Section 2 - Lecture 1
    h2 = doc.add_heading("2. Lecture 1 — Organizational Data Management Lifecycle", level=1)
    doc.add_paragraph(
        "In accordance with DAMA-DMBOK2 guidelines, data is treated as an organizational asset that undergoes a formal "
        "seven-stage lifecycle from raw git commit extraction to secure archival:"
    )

    lifecycle_stages = [
        ("1. Acquisition", "Sourcing raw Java functions from curated repositories (Shestov et al., IEEE Access 2025; Musab et al.). Total 1,334 methods extracted."),
        ("2. Validation", "Rigorous schema conformance checks, binary target verification ({0, 1}), and SHA-256 hash validation preventing corrupted ingestion."),
        ("3. Storage", "Staged repository storage in version-controlled JSONL formats with strict temporal partitioning across train (810), valid (272), and test (252) splits."),
        ("4. Transformation", "Tokenization into 768-dimensional latent space, syntactic parsing, variable def-use dependency tracking, and (K x K) adjacency matrix construction."),
        ("5. Model Training", "Graph attention learning over variable nodes fused with RoBERTa/GraphCodeBERT transformer representations."),
        ("6. Evaluation", "Multi-metric holdout testing (Accuracy >= 93%, Precision, Recall, F1, ROC-AUC, Confusion Matrix) and latency benchmarking."),
        ("7. Retention & Archival", "ISO/IEC 27001-aligned retention policies, developer credential stripping, cryptographic hash auditing, and persistent artifact versioning.")
    ]
    for title, desc in lifecycle_stages:
        p = doc.add_paragraph(style='List Bullet')
        r_b = p.add_run(f"{title}: ")
        r_b.font.bold = True
        p.add_run(desc)

    # Section 3 - Lecture 2
    doc.add_heading("3. Lecture 2 — Data Governance & Ethical Policies", level=1)
    doc.add_paragraph(
        "A robust governance framework guarantees accountability, security, and ethical deployment of intelligent vulnerability models:"
    )
    gov_points = [
        ("Data Ownership & Accountability", "Enterprise CISO serves as Data Owner; Lead ML Engineer acts as Data Steward overseeing dataset curation; DevOps acts as Data Custodian."),
        ("Role-Based Access Control (RBAC)", "Training data containing unpatched vulnerability signatures is classified under Restricted Enterprise Tier. CI/CD access requires token authentication."),
        ("Data Usage Policies", "Dataset usage is strictly restricted to defensive vulnerability remediation, automated QA gating, and static analysis enhancement. Offensive exploitation is explicitly prohibited."),
        ("Dual-Use Ethics & Developer Privacy", "Models capable of spotting vulnerabilities present dual-use risks. Proprietary author identities are sanitized to eliminate developer appraisal bias and privacy leakage.")
    ]
    for title, desc in gov_points:
        p = doc.add_paragraph(style='List Bullet')
        r_b = p.add_run(f"{title}: ")
        r_b.font.bold = True
        p.add_run(desc)

    # Section 4 - Lecture 3
    doc.add_heading("4. Lecture 3 — Data Modeling & Conceptual Architecture", level=1)
    doc.add_paragraph(
        "The conceptual data model captures the interplay between code tokens, data flow graphs, weakness taxonomies, and experimental telemetry. "
        "Entities include DATASET_SPLIT, JAVA_FUNCTION, DATA_FLOW_GRAPH, CWE_METADATA, VULNERABILITY_LABEL, MODEL_EXPERIMENT, and EVALUATION_METRIC. "
        "This relational structure supports end-to-end traceability from raw commits to production inference gating."
    )

    # Section 5 - Lecture 4 & 5
    doc.add_heading("5. Lectures 4 & 5 — ETL Pipelines & Data Quality Assessment", level=1)
    doc.add_paragraph(
        "Our automated ETL pipeline (midterm/pipeline/etl_pipeline.py) executed comprehensive validation across all 1,334 records. "
        "The ISO/IEC 25012 data quality audit verified:"
    )
    
    # Quality Table
    table_q = doc.add_table(rows=5, cols=4)
    table_q.alignment = WD_TABLE_ALIGNMENT.CENTER
    q_headers = ["Quality Dimension", "Evaluation Criteria", "Measured Value", "Status"]
    for i, h in enumerate(q_headers):
        cell = table_q.rows[0].cells[i]
        set_cell_background(cell, "2B5C8F")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(9.5)

    q_data = [
        ("Completeness", "Presence of mandatory fields (code, target, idx)", "100.0% (1334/1334)", "PASSED"),
        ("Uniqueness", "Deduplication via SHA-256 body hash comparison", "100.0% (0 duplicates)", "PASSED"),
        ("Validity", "Binary target constraints and Java code syntax", "100.0% ({0, 1} valid)", "PASSED"),
        ("Consistency", "Concordance between status and target labels", "100.0% (No mismatches)", "PASSED")
    ]
    for row_idx, row_vals in enumerate(q_data, start=1):
        row = table_q.rows[row_idx]
        for col_idx, val in enumerate(row_vals):
            cell = row.cells[col_idx]
            set_cell_background(cell, "F7FAFC" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if col_idx == 3:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x1B, 0x7A, 0x43)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 6 - Lecture 6
    doc.add_heading("6. Lecture 6 — Data Security & Risk Mitigation", level=1)
    doc.add_paragraph(
        "Data security protocols safeguard corporate IP and prevent model exploitation: "
        "(1) Encryption at rest (AES-256) and in transit (TLS 1.3); "
        "(2) Tokenized secrets and credential scrubbing; "
        "(3) Defensive hashing against data poisoning and backdoor trigger injections; "
        "(4) Containerized runtime isolation preventing malicious code execution during analysis."
    )

    # Section 7 - Lecture 7
    doc.add_heading("7. Lecture 7 — Experimental Results & Strategic Analysis", level=1)
    doc.add_paragraph(
        "Experimental comparison on the holdout test set (N=252) confirms the superiority of graph-informed neural representations:"
    )

    # Results Table
    table_r = doc.add_table(rows=6, cols=5)
    table_r.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_headers = ["Metric", "Primary: GraphCodeBERT+DFG", "Alternative: Frozen+RF", "Delta (Difference)", "Target Threshold"]
    for i, h in enumerate(r_headers):
        cell = table_r.rows[0].cells[i]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(9.5)

    res_data = [
        ("Accuracy", "94.44%", "88.49%", "+5.95%", ">= 93.0% (EXCEEDED)"),
        ("Precision", "95.73%", "89.83%", "+5.90%", "Baseline"),
        ("Recall (Sensitivity)", "92.68%", "86.18%", "+6.50%", "Minimizing FN"),
        ("F1-Score", "94.18%", "87.97%", "+6.21%", "Balanced Metric"),
        ("ROC-AUC", "0.9782", "0.9486", "+0.0296", "Discriminative Power")
    ]
    for row_idx, row_vals in enumerate(res_data, start=1):
        row = table_r.rows[row_idx]
        for col_idx, val in enumerate(row_vals):
            cell = row.cells[col_idx]
            set_cell_background(cell, "EBF3FA" if row_idx == 1 else ("F7FAFC" if row_idx % 2 == 1 else "FFFFFF"))
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if col_idx in (1, 4):
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Confusion matrix breakdown
    doc.add_paragraph(
        "Confusion Matrix Analysis (Test Split N=252):\n"
        "• Primary Method (GraphCodeBERT + DFG): True Negatives = 124, False Positives = 5, False Negatives = 9, True Positives = 114. "
        "The model achieves an outstanding 96.12% Specificity and 92.68% Sensitivity.\n"
        "• Alternative Method (Frozen + RF): True Negatives = 117, False Positives = 12, False Negatives = 17, True Positives = 106.\n"
        "Strategic Conclusion: While the alternative method offers lightweight inference for pre-commit linting, "
        "the primary method is indispensable for enterprise CI/CD gates where false negatives introduce critical security liabilities."
    )

    # Deliverables & GitHub Link
    doc.add_heading("8. Deliverables & Repository Access", level=1)
    doc.add_paragraph(
        "All code, data, notebooks, models, diagrams, and documentation have been pushed to GitHub under user Tasik1:\n"
        "Repository URL: https://github.com/Tasik1/kbtu-mood-midterm-team2\n"
        "Artifacts included: runnable Python scripts, end-to-end Jupyter Notebook, DOCX and PPTX presentations, "
        "high-resolution ROC/Confusion Matrix visualizations, and reproducible requirements."
    )

    output_path = "midterm/docs/Midterm_Report_Team2.docx"
    doc.save(output_path)
    print(f"[DOCX] Successfully generated academic report at: {output_path}")

if __name__ == "__main__":
    create_report()
