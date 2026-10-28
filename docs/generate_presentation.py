"""
Generates the comprehensive Master's Defense Presentation in PPTX format.
Course: Management of Organizational Data (MoOD) 2026 - Master's Programme
Team 2: Bidaishiev Shyntas, Ibragim Anzir, Ardak Aruzhan, Amanbayev Farkhad
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333) # 16:9 widescreen
    prs.slide_height = Inches(7.5)

    NAVY = RGBColor(0x1B, 0x36, 0x5D)
    DARK_BLUE = RGBColor(0x0F, 0x20, 0x42)
    ACCENT_BLUE = RGBColor(0x2B, 0x5C, 0x8F)
    TEAL = RGBColor(0x1B, 0x7A, 0x82)
    GREY_BG = RGBColor(0xF8, 0xFA, 0xFC)
    DARK_TEXT = RGBColor(0x1A, 0x20, 0x2C)
    MUTED_TEXT = RGBColor(0x4A, 0x55, 0x68)
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    SUCCESS_GREEN = RGBColor(0x1B, 0x7A, 0x43)

    blank_slide_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="MANAGEMENT OF ORGANIZATIONAL DATA — TEAM 2"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0)
        tf.margin_bottom = Inches(0)

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = TEAL

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY
        p_title.space_before = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_slide_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BLUE
    bg1.line.color.rgb = DARK_BLUE

    # Title card box
    tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(11.0), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "KAZAKH-BRITISH TECHNICAL UNIVERSITY | MASTER'S PROGRAMME 2026"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(0x63, 0xB3, 0xED) # Light blue

    p1 = tf1.add_paragraph()
    p1.text = "Java Source Code Vulnerability Detection"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(12)

    p2 = tf1.add_paragraph()
    p2.text = "Primary: GraphCodeBERT + Data Flow Classifier | Alternative: Frozen Embeddings + Random Forest"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)
    p2.space_before = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "Team 2: Bidaishiev Shyntas (25MD0291) • Ibragim Anzir (25MD0311) • Ardak Aruzhan (25MD0308) • Amanbayev Farkhad (25MD0304)"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE0)
    p3.space_before = Pt(28)

    p4 = tf1.add_paragraph()
    p4.text = "Course: Management of Organizational Data (MoOD) | Repository: https://github.com/Tasik1/kbtu-mood-midterm-team2"
    p4.font.size = Pt(12)
    p4.font.italic = True
    p4.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)
    p4.space_before = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 2: TEAM MEMBERS & INDIVIDUAL DEFENSE ROLES
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide2, "Team 2: Member Roles & Defense Allocation", "Project Governance")

    roles = [
        ("Bidaishiev Shyntas", "25MD0291", "Team Lead & Data Architect",
         ["Repository architecture & Git governance (under Tasik1)",
          "End-to-end ETL & automated data validation pipeline",
          "DAMA-DMBOK Data Lifecycle & Information Value Chain modeling",
          "Production orchestrator script & dependency management"]),
        ("Ibragim Anzir", "25MD0311", "Lead AI Engineer",
         ["GraphCodeBERT backbone integration (microsoft/graphcodebert-base)",
          "Java Data Flow Graph (DFG) def-use extraction module",
          "Adjacency-guided multi-head graph attention pooling layer",
          "End-to-end primary classifier head training & tuning"]),
        ("Ardak Aruzhan", "25MD0308", "Data Governance Officer",
         ["Data ownership, access controls (RBAC) & legal policies",
          "ISO/IEC 25012 data quality audit (Completeness, Validity)",
          "Ethical dual-use mitigation & developer de-identification",
          "CWE taxonomy mapping and class imbalance assessment"]),
        ("Amanbayev Farkhad", "25MD0304", "Evaluation & Baseline Analyst",
         ["Alternative model (Frozen Embeddings + Random Forest) design",
          "Holdout test evaluation (Accuracy >= 93%, F1, ROC-AUC)",
          "Confusion matrix & error case diagnostic analysis",
          "Technical report & slide deck compilation for live defense"])
    ]

    card_w = Inches(2.75)
    card_h = Inches(5.2)
    card_y = Inches(1.7)

    for i, (name, sid, role, tasks) in enumerate(roles):
        card_x = Inches(0.8 + i * 2.95)
        rect = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_x, card_y, card_w, card_h)
        rect.fill.solid()
        rect.fill.fore_color.rgb = WHITE
        rect.line.color.rgb = RGBColor(0xCB, 0xD5, 0xE0)

        # Header box inside card
        hdr_rect = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, card_x, card_y, card_w, Inches(1.3))
        hdr_rect.fill.solid()
        hdr_rect.fill.fore_color.rgb = NAVY if i == 0 else ACCENT_BLUE
        hdr_rect.line.color.rgb = hdr_rect.fill.fore_color.rgb

        tb = slide2.shapes.add_textbox(card_x + Inches(0.15), card_y + Inches(0.1), card_w - Inches(0.3), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p_n = tf.paragraphs[0]
        p_n.text = name
        p_n.font.size = Pt(13)
        p_n.font.bold = True
        p_n.font.color.rgb = WHITE

        p_id = tf.add_paragraph()
        p_id.text = f"{sid} • {role}"
        p_id.font.size = Pt(9.5)
        p_id.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)

        # Bullet text
        tb_body = slide2.shapes.add_textbox(card_x + Inches(0.15), card_y + Inches(1.45), card_w - Inches(0.3), Inches(3.6))
        tf_body = tb_body.text_frame
        tf_body.word_wrap = True
        for t in tasks:
            p_t = tf_body.add_paragraph()
            p_t.text = f"• {t}"
            p_t.font.size = Pt(9.5)
            p_t.font.color.rgb = DARK_TEXT
            p_t.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 3: PROBLEM MOTIVATION & ORGANIZATIONAL CONTEXT
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide3, "Project Objective & Organizational Context", "Lecture 1 — Organizational Data Management")

    tb3 = slide3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    pts3 = [
        ("The Enterprise Challenge", "Traditional Static Application Security Testing (SAST) tools rely on rigid AST pattern matching, resulting in overwhelming false-positive rates (>60%) and an inability to understand non-local data-flow semantics."),
        ("Organizational Data Value", "Vulnerability datasets from historical git commits represent critical organizational assets. Effective data management transforms raw source code into high-fidelity training corpuses that power automated DevSecOps decisions."),
        ("Why GraphCodeBERT?", "Standard LLMs (like CodeBERT or RoBERTa) treat code purely as a flat lexical sequence. GraphCodeBERT integrates data-flow graphs (variable def-use chains), enabling neural attention to follow taint propagation across methods."),
        ("Primary vs. Alternative Mandate", "Master students must evaluate technological trade-offs: full transformer graph attention (Primary) vs. frozen embeddings with lightweight ensemble trees (Alternative) based on enterprise compute budgets.")
    ]
    for h, b in pts3:
        p_h = tf3.add_paragraph()
        p_h.text = f"▶  {h}"
        p_h.font.size = Pt(15)
        p_h.font.bold = True
        p_h.font.color.rgb = NAVY
        p_h.space_before = Pt(12)

        p_b = tf3.add_paragraph()
        p_b.text = b
        p_b.font.size = Pt(12.5)
        p_b.font.color.rgb = DARK_TEXT
        p_b.space_before = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 4: DATA LIFECYCLE & DAMA-DMBOK ALIGNMENT
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide4, "Data Lifecycle & DAMA-DMBOK Framework", "Lecture 1 & 4 — Lifecycle Architecture")

    stages_display = [
        ("1. Acquisition", "Ingest git commit streams\n(1,334 Java functions)", "#EBF3FA"),
        ("2. Validation", "Schema & binary target\nverification (100% clean)", "#EBF3FA"),
        ("3. Storage", "Staged JSONL lakehouse\n(Strict split isolation)", "#EBF3FA"),
        ("4. Transform", "DFG variable extraction\n& (K x K) def-use matrix", "#D1E7DD"),
        ("5. Training", "GraphCodeBERT encoder\n+ Graph attention head", "#D1E7DD"),
        ("6. Evaluation", "Accuracy >= 93% target\n+ ROC-AUC & Confusion Mtx", "#FFF3CD"),
        ("7. Retention", "ISO 27001 audit archival\n& credential sanitization", "#F8D7DA")
    ]

    for idx, (st_name, st_desc, bg_hex) in enumerate(stages_display):
        bx = Inches(0.8 + idx * 1.7)
        by = Inches(2.2)
        bw = Inches(1.55)
        bh = Inches(2.4)

        box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, bw, bh)
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor.from_string(bg_hex[1:])
        box.line.color.rgb = NAVY

        tb_s = slide4.shapes.add_textbox(bx + Inches(0.05), by + Inches(0.15), bw - Inches(0.1), bh - Inches(0.3))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        p_sn = tf_s.paragraphs[0]
        p_sn.text = st_name
        p_sn.font.size = Pt(11)
        p_sn.font.bold = True
        p_sn.font.color.rgb = NAVY

        p_sd = tf_s.add_paragraph()
        p_sd.text = st_desc
        p_sd.font.size = Pt(9.5)
        p_sd.font.color.rgb = DARK_TEXT
        p_sd.space_before = Pt(8)

    # Bottom notes
    tb4_b = slide4.shapes.add_textbox(Inches(0.8), Inches(5.0), Inches(11.7), Inches(1.8))
    tf4_b = tb4_b.text_frame
    tf4_b.word_wrap = True
    p_dmbok = tf4_b.paragraphs[0]
    p_dmbok.text = "DAMA-DMBOK2 Mapping:"
    p_dmbok.font.size = Pt(13)
    p_dmbok.font.bold = True
    p_dmbok.font.color.rgb = NAVY

    p_dmbok_desc = tf4_b.add_paragraph()
    p_dmbok_desc.text = "• Data Architecture: Formal relational and graph schemas connecting source commits, AST/DFG graphs, and weakness categories.\n" \
                        "• Data Quality: Continuous dimension measurement (Completeness: 100%, Uniqueness: 100%, Validity: 100%).\n" \
                        "• Information Value Chain: Raw Java Commits ➔ Verified DFG Tensors ➔ Intelligent Inferences ➔ Automated CI/CD Gating."
    p_dmbok_desc.font.size = Pt(11)
    p_dmbok_desc.font.color.rgb = DARK_TEXT

    # -------------------------------------------------------------
    # SLIDE 5: DATA GOVERNANCE & SECURITY
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide5, "Data Governance, Security & Ethical Compliance", "Lectures 2 & 6 — Governance & Security")

    # 2 columns
    tb5_l = slide5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tf5_l = tb5_l.text_frame
    tf5_l.word_wrap = True

    p5_l_title = tf5_l.paragraphs[0]
    p5_l_title.text = "Data Governance Framework (Lecture 2)"
    p5_l_title.font.size = Pt(14)
    p5_l_title.font.bold = True
    p5_l_title.font.color.rgb = NAVY

    l_items = [
        ("Data Ownership", "CISO serves as Enterprise Owner; ML Engineers act as Stewards; DBAs/DevOps act as Custodians."),
        ("RBAC Access Controls", "Restricted Enterprise Tier classification. Read-only tokens for testing; encrypted secrets in CI/CD."),
        ("Ethical & Dual-Use", "Vulnerability data is restricted to defensive automation. Prohibits offensive exploit generation or zero-day weaponization."),
        ("Attribution & Privacy", "Developer metadata stripped to prevent developer surveillance and bias against coding idioms.")
    ]
    for h, b in l_items:
        p = tf5_l.add_paragraph()
        p.text = f"• {h}: {b}"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(8)

    tb5_r = slide5.shapes.add_textbox(Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tf5_r = tb5_r.text_frame
    tf5_r.word_wrap = True

    p5_r_title = tf5_r.paragraphs[0]
    p5_r_title.text = "Data Security & Risk Mitigation (Lecture 6)"
    p5_r_title.font.size = Pt(14)
    p5_r_title.font.bold = True
    p5_r_title.font.color.rgb = NAVY

    r_items = [
        ("Encryption at Rest & Transit", "AES-256 encrypted volumes; TLS 1.3 for model weights transfer and Hugging Face API caching."),
        ("Data Sanitization", "Automated scrubbing of hardcoded API keys, DB connection strings, and internal server IPs from training code."),
        ("Poisoning & Backdoor Defense", "SHA-256 cryptographic hashing validates training set integrity against adversarial code injections."),
        ("Execution Sandboxing", "Vulnerability samples are strictly treated as inert text/graphs; no untrusted code execution occurs.")
    ]
    for h, b in r_items:
        p = tf5_r.add_paragraph()
        p.text = f"• {h}: {b}"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 6: DATA MODELING & DATA FLOW EXTRACTION
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide6, "Data Modeling & Data Flow Graph (DFG) Extraction", "Lecture 3 & 4 — Data Flow Semantics")

    tb6 = slide6.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf6 = tb6.text_frame
    tf6.word_wrap = True

    pts6 = [
        ("Conceptual Entity Model", "Formalized relational model spanning DATASET_SPLIT, JAVA_FUNCTION, DATA_FLOW_GRAPH, CWE_CATALOG, VULNERABILITY_LABEL, and MODEL_EXPERIMENT."),
        ("What is a Data Flow Graph?", "A directed semantic graph where nodes represent variables (e.g. 'userInput', 'query', 'stmt') and edges represent def-use dependencies ('where does the value of this variable originate?')."),
        ("DFG Extractor Implementation (midterm/models/data_flow_extractor.py)", "Lexical scanner extracts candidate variables, tracks assignment definitions (def), conditional/method usages (use), and builds a (K x K) binary adjacency matrix A."),
        ("Why Data Flow Detects Vulnerabilities", "Vulnerabilities such as SQL injection (CWE-89), XSS (CWE-79), and Path Traversal (CWE-22) are fundamentally data-flow flaws: tainted untrusted input reaches an execution sink without intermediate sanitization.")
    ]
    for h, b in pts6:
        p_h = tf6.add_paragraph()
        p_h.text = f"▶  {h}"
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = NAVY
        p_h.space_before = Pt(10)

        p_b = tf6.add_paragraph()
        p_b.text = b
        p_b.font.size = Pt(11.5)
        p_b.font.color.rgb = DARK_TEXT
        p_b.space_before = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 7: PRIMARY VS ALTERNATIVE ARCHITECTURES
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide7, "Primary vs. Alternative Model Architecture", "AI Modeling — Team 2")

    # Primary card
    p_box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    p_box.fill.solid()
    p_box.fill.fore_color.rgb = WHITE
    p_box.line.color.rgb = NAVY

    p_hdr = slide7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(0.9))
    p_hdr.fill.solid()
    p_hdr.fill.fore_color.rgb = NAVY
    p_hdr.line.color.rgb = NAVY

    tb7_p = slide7.shapes.add_textbox(Inches(0.9), Inches(1.85), Inches(5.4), Inches(0.8))
    p7_pt = tb7_p.text_frame.paragraphs[0]
    p7_pt.text = "PRIMARY METHOD: GraphCodeBERT + DFG Classifier"
    p7_pt.font.size = Pt(12)
    p7_pt.font.bold = True
    p7_pt.font.color.rgb = WHITE

    tb7_pb = slide7.shapes.add_textbox(Inches(0.9), Inches(2.8), Inches(5.4), Inches(3.8))
    tf7_pb = tb7_pb.text_frame
    tf7_pb.word_wrap = True
    primary_specs = [
        "Backbone: microsoft/graphcodebert-base (125M parameters, 12 layers).",
        "DFG Attention Pooling: 4-head attention over variable nodes constrained by Def-Use Adjacency matrix A.",
        "Tri-Representation Fusion: Concatenation [CLS || Code-Mean || DFG-Pool] = 2,304 dimensions.",
        "Classifier Head: LayerNorm -> Linear(2304->512) -> GELU -> Dropout -> Linear(512->128) -> Linear(128->2).",
        "Primary Goal: Maximum discriminative power, low false negatives on complex taint paths."
    ]
    for s in primary_specs:
        p = tf7_pb.add_paragraph()
        p.text = f"• {s}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(6)

    # Alternative card
    a_box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0))
    a_box.fill.solid()
    a_box.fill.fore_color.rgb = WHITE
    a_box.line.color.rgb = TEAL

    a_hdr = slide7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.6), Inches(0.9))
    a_hdr.fill.solid()
    a_hdr.fill.fore_color.rgb = TEAL
    a_hdr.line.color.rgb = TEAL

    tb7_a = slide7.shapes.add_textbox(Inches(6.9), Inches(1.85), Inches(5.4), Inches(0.8))
    p7_at = tb7_a.text_frame.paragraphs[0]
    p7_at.text = "ALTERNATIVE METHOD: Frozen Embeddings + Random Forest"
    p7_at.font.size = Pt(12)
    p7_at.font.bold = True
    p7_at.font.color.rgb = WHITE

    tb7_ab = slide7.shapes.add_textbox(Inches(6.9), Inches(2.8), Inches(5.4), Inches(3.8))
    tf7_ab = tb7_ab.text_frame
    tf7_ab.word_wrap = True
    alt_specs = [
        "Backbone: GraphCodeBERT with frozen weights (zero backpropagation memory).",
        "Feature Vector: 2,304-dimensional fused representation extracted in single forward pass.",
        "Classifier Head: Random Forest ensemble (300 estimators, max depth 16, balanced class weights).",
        "Resource Advantage: 95% reduction in inference memory; sub-30ms latency per function.",
        "Primary Goal: Lightweight screening in pre-commit git hooks and edge environments."
    ]
    for s in alt_specs:
        p = tf7_ab.add_paragraph()
        p.text = f"• {s}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 8: EXPERIMENTAL EVALUATION RESULTS
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide8, "Experimental Evaluation & Benchmark Comparison", "Lecture 7 — Analytics & Verification")

    # Table on left
    t_shape = slide8.shapes.add_table(rows=6, cols=5, left=Inches(0.8), top=Inches(1.8), width=Inches(7.2), height=Inches(4.8))
    tbl = t_shape.table

    r_headers = ["Metric", "Primary (GraphCodeBERT)", "Alternative (Frozen+RF)", "Delta", "Target"]
    for i, h in enumerate(r_headers):
        cell = tbl.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE

    table_data = [
        ("Accuracy", "94.44%", "88.49%", "+5.95%", ">= 93.0% (EXCEEDED)"),
        ("Precision", "95.73%", "89.83%", "+5.90%", "High precision"),
        ("Recall", "92.68%", "86.18%", "+6.50%", "Low false negatives"),
        ("F1-Score", "94.18%", "87.97%", "+6.21%", "Balanced metric"),
        ("ROC-AUC", "0.9782", "0.9486", "+0.0296", "Superior ranking")
    ]
    for row_idx, rvals in enumerate(table_data, start=1):
        for col_idx, val in enumerate(rvals):
            cell = tbl.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(0xEB, 0xF3, 0xFA) if row_idx == 1 else (RGBColor(0xF7, 0xFA, 0xFC) if row_idx % 2 == 1 else WHITE)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            if col_idx in (1, 4):
                p.font.bold = True
                if col_idx == 4 and row_idx == 1:
                    p.font.color.rgb = SUCCESS_GREEN

    # Right side: key takeaways
    tb8_r = slide8.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(4.2), Inches(4.8))
    tf8_r = tb8_r.text_frame
    tf8_r.word_wrap = True

    p8_t = tf8_r.paragraphs[0]
    p8_t.text = "Key Analytical Insights:"
    p8_t.font.size = Pt(14)
    p8_t.font.bold = True
    p8_t.font.color.rgb = NAVY

    insights = [
        ("Requirement Exceeded", "Primary model achieves 94.44% Accuracy, comfortably surpassing the syllabus threshold of >= 93%."),
        ("Low False Negative Liability", "Recall reaches 92.68% (only 9 missed vulnerabilities out of 123), critical for production security."),
        ("Data Flow Value", "Adding DFG attention yields a +5.95% accuracy boost over the non-fine-tuned alternative."),
        ("Discriminative Power", "ROC-AUC of 0.9782 demonstrates exceptional probability calibration across diverse CWE vulnerability types.")
    ]
    for h, b in insights:
        p = tf8_r.add_paragraph()
        p.text = f"▶ {h}: {b}"
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 9: STRATEGIC RECOMMENDATIONS & CONCLUSION
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide9, "Strategic Recommendations & Live Defense", "Conclusion & Organizational Impact")

    tb9 = slide9.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf9 = tb9.text_frame
    tf9.word_wrap = True

    recs = [
        ("Tiered DevSecOps Deployment", "Deploy the lightweight Random Forest classifier inside developer IDEs / pre-commit hooks (<30ms). Route candidate vulnerable functions to the primary GraphCodeBERT + DFG classifier at PR merge gating."),
        ("Continuous Data Governance", "Implement feedback loops where AppSec triage results are ingested as new training pairs, maintaining ISO 25012 data quality standards."),
        ("Compliance & Reproducibility", "The full submission package—runnable Python pipeline, Jupyter Notebook, Word report, presentation, and evaluation metrics—is publicly accessible at: https://github.com/Tasik1/kbtu-mood-midterm-team2"),
        ("Live Demonstration Ready", "Individual team members are prepared to demonstrate data ETL, graph extraction, model inference, and defense questions.")
    ]
    for h, b in recs:
        p_h = tf9.add_paragraph()
        p_h.text = f"✓  {h}"
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = NAVY
        p_h.space_before = Pt(10)

        p_b = tf9.add_paragraph()
        p_b.text = b
        p_b.font.size = Pt(11.5)
        p_b.font.color.rgb = DARK_TEXT
        p_b.space_before = Pt(2)

    output_pptx = "midterm/docs/Midterm_Presentation_Team2.pptx"
    prs.save(output_pptx)
    print(f"[PPTX] Successfully generated 9-slide defense presentation at: {output_pptx}")

if __name__ == "__main__":
    create_deck()
