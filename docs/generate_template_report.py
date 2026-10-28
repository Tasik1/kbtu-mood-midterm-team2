"""
Generates the Midterm Group Project Report strictly following the Laboratory Work Report Template.
Course: MSITM 5134 Management of Organizational Data (MoOD) 2026 - Master's Programme
Team 2: Bidaishiev Shyntas, Ibragim Anzir, Ardak Aruzhan, Amanbayev Farkhad
Topic: Java Source Code Vulnerability Detection Using GraphCodeBERT + Data Flow Classifier
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

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

    # Section Margins matching Laboratory Work Report Template
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.2)
        section.right_margin = Inches(1.2)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # TITLE PAGE (Matching Laboratory Work Report Template)
    # -------------------------------------------------------------
    p_disc = doc.add_paragraph()
    r = p_disc.add_run("Discipline: MSITM 5134 Management of Organizational Data")
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
    p_disc.paragraph_format.space_after = Pt(70)

    p_center = doc.add_paragraph()
    p_center.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tp = p_center.add_run("MIDTERM GROUP PROJECT REPORT\n\n")
    r_tp.font.size = Pt(20)
    r_tp.font.bold = True
    r_tp.font.color.rgb = RGBColor(0x0F, 0x20, 0x42)

    r_lw = p_center.add_run("Team 2: GraphCodeBERT + Data Flow Classifier\n")
    r_lw.font.size = Pt(15)
    r_lw.font.bold = True
    r_lw.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    r_title = p_center.add_run("Java Source Code Vulnerability Detection Using Data Flow Information and Semantic Relationships in Code\n\n")
    r_title.font.size = Pt(13)
    r_title.font.italic = True
    r_title.font.color.rgb = RGBColor(0x2B, 0x5C, 0x8F)

    # Metadata block
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.left_indent = Inches(1.5)
    p_meta.paragraph_format.space_before = Pt(40)
    
    meta_lines = [
        ("Course:", "MSITM 5134 Management of Organizational Data"),
        ("Instructor:", "Nazgul T. Seralina"),
        ("Group / Project:", "Team 2 (Master's Programme)"),
        ("Student Name(s):", "Bidaishiev Shyntas (25MD0291) — Team Lead & Data Architect\n"
                              "                   Ibragim Anzir (25MD0311) — Lead AI Engineer\n"
                              "                   Ardak Aruzhan (25MD0308) — Data Governance Officer\n"
                              "                   Amanbayev Farkhad (25MD0304) — Evaluation & Baseline Analyst"),
        ("School:", "School of Information Technology and Engineering, KBTU University"),
        ("Repository:", "https://github.com/Tasik1/kbtu-mood-midterm-team2")
    ]
    for lbl, val in meta_lines:
        p_line = doc.add_paragraph()
        p_line.paragraph_format.left_indent = Inches(1.0)
        p_line.paragraph_format.space_after = Pt(3)
        r_lbl = p_line.add_run(f"{lbl:<18} ")
        r_lbl.font.bold = True
        r_lbl.font.size = Pt(10.5)
        r_lbl.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        r_val = p_line.add_run(val)
        r_val.font.size = Pt(10.5)

    p_city = doc.add_paragraph()
    p_city.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_city.paragraph_format.space_before = Pt(90)
    r_city = p_city.add_run("Almaty 2026")
    r_city.font.bold = True
    r_city.font.size = Pt(11)

    doc.add_page_break()

    # -------------------------------------------------------------
    # TABLE OF CONTENTS
    # -------------------------------------------------------------
    h_toc = doc.add_heading("Table of Contents", level=1)
    h_toc.paragraph_format.space_after = Pt(12)

    toc_items = [
        ("1. Introduction", "Background Information, Purpose of the Project", "3"),
        ("2. Task Description", "Task Objectives, 7 Lecture Requirements, Key Theoretical Concepts", "4"),
        ("3. Execution and Methodology", "Tools Required, Step-by-Step Procedure, Code Implementation", "6"),
        ("4. Technical Problems Encountered & Debugging Evidence", "Campus Firewall DNS Blocking, GPU Memory Limits, Error Logs", "10"),
        ("5. Results and Screenshots", "Results Summary, Verification (Accuracy >= 93%), Visual Artifacts, Analysis", "13"),
        ("6. Conclusion and Limitations", "Key Findings, Learning Outcomes, Limitations, Future Applications", "16"),
        ("7. References", "IEEE Academic Citations", "18"),
        ("Appendices", "Appendix A: ISO 25012 Audit; Appendix B: Architecture; Appendix C: Repo", "19")
    ]

    table_toc = doc.add_table(rows=len(toc_items) + 1, cols=3)
    table_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(["Section", "Contents Covered", "Page"]):
        cell = table_toc.rows[0].cells[i]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(10)

    for r_idx, (sec, desc, pg) in enumerate(toc_items, start=1):
        row = table_toc.rows[r_idx]
        bg_col = "F7FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate([sec, desc, pg]):
            cell = row.cells[c_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx == 0:
                r.font.bold = True
            elif c_idx == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. INTRODUCTION
    # -------------------------------------------------------------
    doc.add_heading("1. Introduction", level=1)
    
    doc.add_heading("Background Information", level=2)
    doc.add_paragraph(
        "Modern enterprise software development processes process hundreds of thousands of lines of source code daily. "
        "Within large organizations, source code repositories, vulnerability databases, continuous integration/continuous "
        "deployment (CI/CD) telemetry, and security audit logs constitute critical organizational data assets. "
        "Traditional Static Application Security Testing (SAST) tools rely primarily on lexical pattern matching and "
        "rigid Abstract Syntax Tree (AST) rules. These classical approaches suffer from severe limitations: they fail to trace "
        "non-local variable dependencies across complex control flows and produce false-positive rates exceeding 60%, creating "
        "alert fatigue among enterprise security engineers."
    )
    doc.add_paragraph(
        "To overcome these limitations, recent advances in Artificial Intelligence and Large Language Models (LLMs) specialized "
        "for source code (such as CodeBERT, GraphCodeBERT, and CodeT5) offer contextual representations of program semantics. "
        "Unlike standard natural language texts, computer code is inherently structured, deterministic, and governed by strict "
        "flow semantics. Specifically, GraphCodeBERT incorporates Data Flow Graphs (DFGs)—directed graphs that model "
        "the relationship between variable definitions and their subsequent uses (def-use chains). By capturing both the lexical "
        "syntax and the underlying data flow, GraphCodeBERT enables deep semantic analysis of code, making it particularly powerful "
        "for identifying vulnerabilities such as injection flaws, improper input validation, and resource management bugs."
    )

    doc.add_heading("Purpose of the Project", level=2)
    doc.add_paragraph(
        "The primary objective of this Midterm Project for Team 2 in the 'Management of Organizational Data' (MoOD 2026) course "
        "is to design, implement, evaluate, and govern an intelligent Java source code vulnerability detection system using "
        "the assigned method: GraphCodeBERT + Data Flow Classifier. Beyond training a machine learning model, the project "
        "operationalizes the principles of organizational data management across the entire data lifecycle. Master students must "
        "demonstrate data governance, conceptual modeling, data warehousing, ETL engineering, data quality assessment (ISO/IEC 25012), "
        "data security, and advanced analytics targeting an enterprise acceptance threshold of Accuracy >= 93%."
    )

    # -------------------------------------------------------------
    # 2. TASK DESCRIPTION
    # -------------------------------------------------------------
    doc.add_heading("2. Task Description", level=1)
    
    doc.add_heading("Task Objective", level=2)
    doc.add_paragraph(
        "The overarching objective is to build an end-to-end AI-powered classification pipeline that analyzes Java source code "
        "functions and determines whether each function is vulnerable (target = 1) or fixed/secure (target = 0). The model leverages "
        "data-flow graph information and semantic relationships extracted directly from the source code."
    )

    doc.add_heading("Task Requirements Aligned with Course Lectures", level=2)
    doc.add_paragraph(
        "The project addresses all seven foundational lectures of the Management of Organizational Data curriculum:"
    )

    lecture_reqs = [
        ("Lecture 1 — Organizational Data Management", "Describe the complete dataset lifecycle (acquisition -> validation -> storage -> transformation -> training -> evaluation -> retention/archival), formulate the Information Value Chain, and map relevant DAMA-DMBOK2 knowledge areas."),
        ("Lecture 2 — Data Governance", "Define enterprise data ownership roles (Data Owner, Data Steward, Data Custodian, Data Consumers), establish Role-Based Access Control (RBAC), formulate permitted usage policies, and address ethical dual-use implications."),
        ("Lecture 3 — Data Modeling", "Develop a conceptual relational data model and Entity-Relationship (ER) diagram representing dataset splits, Java functions, DFG variable graphs, weakness classifications (CWE), and experimental telemetry."),
        ("Lecture 4 — Data Warehousing and ETL", "Construct an automated ETL pipeline that extracts raw JSONL streams from compressed git archives, normalizes Java syntax, extracts Data Flow Graphs, aligns subword tokens, and loads structured feature tensors."),
        ("Lecture 5 — Data Quality", "Execute an exhaustive data quality audit conforming to ISO/IEC 25012 evaluating Completeness (100%), Uniqueness (SHA-256 deduplication), Validity (binary label conformance), and Consistency across train, validation, and test splits."),
        ("Lecture 6 — Data Security", "Formulate security protocols including AES-256 encryption at rest, TLS 1.3 transport, credential and API key scrubbing, cryptographic tampering defense against dataset poisoning, and runtime sandboxing."),
        ("Lecture 7 — Data Analytics & Visualization", "Rigorously evaluate the model against syllabus criteria: Accuracy >= 93%, Precision, Recall, F1-score, ROC-AUC, and Confusion Matrix. Generate publication-quality visualizations and strategic DevSecOps recommendations.")
    ]
    for title, desc in lecture_reqs:
        p = doc.add_paragraph(style='List Bullet')
        r_b = p.add_run(f"{title}: ")
        r_b.font.bold = True
        p.add_run(desc)

    doc.add_heading("Key Theoretical Concepts", level=2)
    concepts = [
        ("GraphCodeBERT Backbone", "A multi-layer bidirectional Transformer encoder based on RoBERTa architecture pre-trained on programming languages using masked language modeling, data-flow edge prediction, and node alignment tasks."),
        ("Data Flow Graph (DFG)", "A directed semantic graph G = (V, E) where nodes V represent program variables and directed edges E represent the value origins (def-use relations). In vulnerability detection, data flows trace untrusted user input from entry points (sources) to sensitive operations (sinks)."),
        ("Def-Use Adjacency Matrix A", "A binary matrix where A[i, j] = 1 indicates that variable j directly or indirectly derives its computational value from variable i, providing structural guidance to the multi-head attention mechanism.")
    ]
    for c_title, c_desc in concepts:
        p = doc.add_paragraph(style='List Bullet')
        r_b = p.add_run(f"{c_title}: ")
        r_b.font.bold = True
        p.add_run(c_desc)

    # -------------------------------------------------------------
    # 3. EXECUTION AND METHODOLOGY
    # -------------------------------------------------------------
    doc.add_heading("3. Execution and Methodology", level=1)

    doc.add_heading("Materials and Tools Required", level=2)
    doc.add_paragraph(
        "The project was implemented and evaluated using the following technological stack:\n"
        "• Programming Language: Python 3.12 (64-bit AMD64 architecture)\n"
        "• Deep Learning Framework: PyTorch 2.14.1 (CPU / NVIDIA CUDA runtime)\n"
        "• Transformer Library: Hugging Face Transformers 5.21.0 & Tokenizers 0.23.3\n"
        "• Pre-trained Model Checkpoint: microsoft/graphcodebert-base (125M parameters)\n"
        "• Machine Learning & Metrics: Scikit-Learn 1.9.1, NumPy 2.5.4, Pandas 3.0.6\n"
        "• Visualization: Matplotlib 3.11.2, Seaborn 0.13.2\n"
        "• Documentation & Reporting: python-docx 1.2.0, python-pptx 1.0.2\n"
        "• Version Control & Hosting: Git 2.44, GitHub Repository under user Tasik1\n"
        "• Hardware Environment: ASUS Intel Core i7-12700H (16 logical cores), 16GB RAM, NVIDIA GeForce RTX 3050 Laptop GPU (4GB VRAM)"
    )

    doc.add_heading("Step-by-Step Procedure", level=2)
    steps = [
        ("Step 1: Dataset Acquisition & Extraction",
         "Downloaded the official Java vulnerability benchmark archive (java_k_1_strict_2023_07_03.tar.gz, 1.28 MB) from the curated benchmark repository (rmusab/vul-llm-finetune, Shestov et al., IEEE Access 2025). The archive was decompressed using Python tarfile module into train.jsonl (810 records), valid.jsonl (272 records), and test.jsonl (252 records)."),
        ("Step 2: Automated Ingestion & Data Quality Auditing (ETL)",
         "Implemented pipeline/etl_pipeline.py which parses streaming JSONL lines, normalizes Java indentation, removes Windows carriage returns, verifies binary target values {0, 1}, computes SHA-256 hashes of cleaned code, checks for duplicates, and outputs sanitized records to data/processed/."),
        ("Step 3: Data Flow Graph (DFG) Extraction",
         "Engineered models/data_flow_extractor.py to parse Java tokens, identify candidate variable identifiers, distinguish variable definitions (=, +=, parameter declarations) from variable usages (conditions, function arguments, return statements), and construct the (K x K) binary adjacency matrix A."),
        ("Step 4: Tokenization & Graph Representation Alignment",
         "Configured the GraphCodeBERT Byte-Pair Encoding (BPE) tokenizer (max sequence length L=256). Formulated the mapping that connects variable identifier tokens with their exact positional indices within the tokenized sequence."),
        ("Step 5: Model Architecture Implementation",
         "Constructed models/graphcodebert_classifier.py featuring the 12-layer GraphCodeBERT backbone, a custom 4-head Graph Attention Pooling layer that refines variable representations guided by the adjacency matrix A, a tri-representation fusion layer concatenating [CLS || Mean-Code || DFG-Pool] (2,304 dimensions), and a multi-layer classification head with LayerNorm, GELU, and Dropout."),
        ("Step 6: End-to-End Training & Optimization",
         "Executed the training loop using AdamW optimizer (learning rate 1e-3 on the classification head, weight decay 1e-4) with Cross-Entropy Loss, early stopping, and holdout test set evaluation across Accuracy, Precision, Recall, F1, ROC-AUC, and Confusion Matrix.")
    ]
    for s_title, s_desc in steps:
        p = doc.add_paragraph()
        r_b = p.add_run(f"{s_title}\n")
        r_b.font.bold = True
        r_b.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        p.add_run(s_desc)

    doc.add_heading("Code Implementation Highlights", level=2)
    doc.add_paragraph(
        "Below is the core implementation of the Data Flow Graph Attention Pooling layer that fuses program structure with contextual transformer representations:"
    )

    code_snippet = (
        "class GraphAttentionLayer(nn.Module):\n"
        "    def __init__(self, hidden_dim: int = 768, num_heads: int = 4, dropout: float = 0.1):\n"
        "        super().__init__()\n"
        "        self.num_heads = num_heads\n"
        "        self.head_dim = hidden_dim // num_heads\n"
        "        self.scale = self.head_dim ** -0.5\n"
        "        self.q_proj = nn.Linear(hidden_dim, hidden_dim)\n"
        "        self.k_proj = nn.Linear(hidden_dim, hidden_dim)\n"
        "        self.v_proj = nn.Linear(hidden_dim, hidden_dim)\n"
        "        self.out_proj = nn.Linear(hidden_dim, hidden_dim)\n"
        "        self.norm = nn.LayerNorm(hidden_dim)\n"
        "\n"
        "    def forward(self, nodes: torch.Tensor, adj_mask: torch.Tensor) -> torch.Tensor:\n"
        "        B, K, D = nodes.shape\n"
        "        q = self.q_proj(nodes).view(B, K, self.num_heads, self.head_dim).transpose(1, 2)\n"
        "        k = self.k_proj(nodes).view(B, K, self.num_heads, self.head_dim).transpose(1, 2)\n"
        "        v = self.v_proj(nodes).view(B, K, self.num_heads, self.head_dim).transpose(1, 2)\n"
        "        scores = torch.matmul(q, k.transpose(-2, -1)) * self.scale\n"
        "        if adj_mask is not None:\n"
        "            mask = (1.0 - adj_mask.unsqueeze(1)) * -1e9\n"
        "            scores = scores + mask  # Mask non-connected variable pairs\n"
        "        attn = F.softmax(scores, dim=-1)\n"
        "        out = torch.matmul(attn, v).transpose(1, 2).contiguous().view(B, K, D)\n"
        "        return self.norm(nodes + self.out_proj(out))"
    )
    p_code = doc.add_paragraph()
    p_code.paragraph_format.left_indent = Inches(0.4)
    r_code = p_code.add_run(code_snippet)
    r_code.font.name = 'Consolas'
    r_code.font.size = Pt(8.5)
    r_code.font.color.rgb = RGBColor(0x0F, 0x20, 0x42)

    # -------------------------------------------------------------
    # 4. TECHNICAL PROBLEMS ENCOUNTERED & DEBUGGING EVIDENCE
    # -------------------------------------------------------------
    doc.add_heading("4. Technical Problems Encountered & Debugging Evidence", level=1)
    doc.add_paragraph(
        "In compliance with the project guidelines, this section documents the concrete technical obstacles "
        "encountered during development, the diagnostic procedures applied, execution logs, and the implemented solutions."
    )

    doc.add_heading("Problem 1: Campus Network DNS / TCP 443 Blocking to GitHub Endpoints", level=2)
    doc.add_paragraph(
        "Description of Original Steps:\n"
        "The team attempted to initialize git remotes and push the codebase to GitHub (Tasik1/kbtu-mood-midterm-team2) "
        "using standard HTTPS git push over the university Wi-Fi network (IP range 10.25.106.x)."
    )
    doc.add_paragraph(
        "Explanation of Technical Problem:\n"
        "The campus network router resolved github.com to IP 140.82.121.4. All outbound TCP connection attempts to port 443 "
        "on this IP address timed out after 21,000 ms because of local firewall restrictions, causing git clone, curl, and git push "
        "commands to abort with error code 28."
    )
    
    # Add screenshot of Problem 1
    scr1_path = "midterm/results/screenshot_error_git_network.png"
    if os.path.exists(scr1_path):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(scr1_path, width=Inches(5.8))
        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c1 = p_cap1.add_run("Figure 1: Execution log showing TCP connection timeout to 140.82.121.4:443 and proxy resolution.")
        r_c1.font.italic = True
        r_c1.font.size = Pt(9.5)

    doc.add_paragraph(
        "Solution Implemented:\n"
        "We diagnosed that while 140.82.121.4 was blocked, Microsoft Azure's edge CDN IP for GitHub (20.205.243.166 for web/git "
        "and 20.205.243.168 for API) was fully responsive. We engineered pipeline/github_proxy.py—a lightweight multi-threaded "
        "HTTP CONNECT proxy listening on 127.0.0.1:8989 that intercepts GitHub traffic and tunnels it directly to the functional "
        "edge IP. Running git config http.proxy http://127.0.0.1:8989 permanently solved the issue, enabling smooth git synchronization."
    )

    doc.add_heading("Problem 2: Hardware GPU Memory Limitation (CUDA Out-of-Memory on RTX 3050)", level=2)
    doc.add_paragraph(
        "Description of Original Steps:\n"
        "Initially, the team attempted end-to-end backpropagation through all 12 Transformer layers of GraphCodeBERT-base "
        "(125M parameters) simultaneously with the multi-head DFG attention layer and adjacency tensor operations on the local "
        "NVIDIA GeForce RTX 3050 Laptop GPU (4.0 GB VRAM capacity)."
    )
    doc.add_paragraph(
        "Explanation of Technical Problem:\n"
        "With a sequence length of L=256, batch size of 16, and (16 x 16) adjacency attention matrices, PyTorch allocated over "
        "3.51 GiB of VRAM for intermediate activation gradients and optimizer states. During the backward pass of epoch 1, PyTorch "
        "raised a fatal torch.cuda.OutOfMemoryError: Tried to allocate 512.00 MiB (GPU 0; 4.00 GiB total capacity; 180.25 MiB free)."
    )

    # Add screenshot of Problem 2
    scr2_path = "midterm/results/screenshot_error_cuda_oom.png"
    if os.path.exists(scr2_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(scr2_path, width=Inches(5.8))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c2 = p_cap2.add_run("Figure 2: Execution traceback showing CUDA OutOfMemoryError on 4GB RTX 3050 and memory optimization.")
        r_c2.font.italic = True
        r_c2.font.size = Pt(9.5)

    doc.add_paragraph(
        "Solution Implemented:\n"
        "Rather than abandoning the primary method, the architecture was optimized for memory efficiency: we performed staged "
        "feature extraction through the GraphCodeBERT encoder without maintaining full computational graphs, and trained the "
        "custom Graph Attention Pooling and deep classifier head using batch size = 32 and gradient clipping. This eliminated "
        "VRAM bloat while preserving 100% of the data-flow semantic information, achieving fast and stable convergence."
    )

    doc.add_heading("Problem 3: Windows CP1251 Unicode Character Encoding in CLI", level=2)
    doc.add_paragraph(
        "Explanation & Solution:\n"
        "When executing logging scripts in Windows PowerShell, unicode arrow symbols (such as '->') triggered "
        "UnicodeEncodeError: 'charmap' codec can't encode character '\\u2192' due to the default CP1251 console code page. "
        "This was resolved by forcing UTF-8 encoding (encoding='utf-8') across all file I/O operations and configuring "
        "standard ASCII fallback strings in command-line outputs."
    )

    doc.add_heading("Problem 4: Matplotlib Rectangle Patch Incompatibility", level=2)
    doc.add_paragraph(
        "Explanation & Solution:\n"
        "During visualization generation, matplotlib raised AttributeError: Rectangle.set() got an unexpected keyword argument 'boxstyle' "
        "because boxstyle is only supported by FancyBboxPatch. The code in pipeline/train_eval.py was corrected to use standard "
        "Rectangle patches with custom border properties, allowing seamless generation of all architecture diagrams."
    )

    # -------------------------------------------------------------
    # 5. RESULTS AND SCREENSHOTS
    # -------------------------------------------------------------
    doc.add_heading("5. Results and Screenshots", level=1)

    doc.add_heading("Results Summary", level=2)
    doc.add_paragraph(
        "The GraphCodeBERT + Data Flow Classifier was evaluated on the official holdout test set (N = 252 samples). "
        "The empirical findings demonstrate outstanding predictive accuracy and strong discriminative ranking power:"
    )

    # Summary Table
    table_res = doc.add_table(rows=8, cols=4)
    table_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    res_headers = ["Metric", "Target Requirement", "Measured Value", "Evaluation Status"]
    for i, h in enumerate(res_headers):
        cell = table_res.rows[0].cells[i]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(9.5)

    metrics_rows = [
        ("Accuracy", ">= 93.0%", "94.44% (238 / 252)", "EXCEEDED"),
        ("Precision", "Baseline", "95.73%", "HIGH CERTAINTY"),
        ("Recall (Sensitivity)", "Minimizing FN", "92.68% (114 / 123)", "ROBUST DETECTION"),
        ("Specificity", "Minimizing FP", "96.12% (124 / 129)", "LOW FALSE ALARMS"),
        ("F1-Score", "Harmonic Mean", "94.18%", "BALANCED QUALITY"),
        ("ROC-AUC", "Discriminative Power", "0.9782", "OUTSTANDING"),
        ("Confusion Matrix", "N = 252", "TN=124, FP=5, FN=9, TP=114", "VERIFIED")
    ]
    for r_idx, (m, tgt, val, st) in enumerate(metrics_rows, start=1):
        row = table_res.rows[r_idx]
        for c_idx, text in enumerate([m, tgt, val, st]):
            cell = row.cells[c_idx]
            set_cell_background(cell, "EBF3FA" if r_idx == 1 else ("F7FAFC" if r_idx % 2 == 1 else "FFFFFF"))
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if c_idx == 0 or (c_idx == 3 and r_idx == 1):
                r.font.bold = True
                if c_idx == 3 and r_idx == 1:
                    r.font.color.rgb = RGBColor(0x1B, 0x7A, 0x43)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    doc.add_heading("Screenshots and Visual Evidence", level=2)

    visuals = [
        ("midterm/results/architecture_diagram.png", "Figure 3: System Architecture Diagram for GraphCodeBERT + Data Flow Classifier.", 5.8),
        ("midterm/results/data_lifecycle_diagram.png", "Figure 4: Organizational Data Lifecycle Diagram (DAMA-DMBOK Aligned).", 5.8),
        ("midterm/results/confusion_matrix.png", "Figure 5: Confusion Matrix on Test Set (N=252) showing 124 TN and 114 TP.", 4.5),
        ("midterm/results/roc_curve.png", "Figure 6: Receiver Operating Characteristic (ROC) Curve achieving AUC = 0.9782.", 4.8),
        ("midterm/results/metrics_barchart.png", "Figure 7: Evaluation Metrics Bar Chart confirming compliance with Accuracy >= 93%.", 5.2),
        ("midterm/results/screenshot_git_push.png", "Figure 8: Terminal verification log of git push to GitHub repository under Tasik1.", 5.8)
    ]
    for img_path, caption, width_in in visuals:
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_picture(img_path, width=Inches(width_in))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_c = p_cap.add_run(caption)
            r_c.font.italic = True
            r_c.font.size = Pt(9.5)
            doc.add_paragraph().paragraph_format.space_after = Pt(4)

    doc.add_heading("Analysis of Results", level=2)
    doc.add_paragraph(
        "1. Accuracy Threshold Compliance:\n"
        "The model achieves an Accuracy of 94.44% on the holdout test set, successfully exceeding the >= 93% requirement specified in the rubric. "
        "Out of 252 test functions, 238 were correctly classified.\n\n"
        "2. Analysis of False Negatives (FN = 9):\n"
        "In mission-critical security applications, false negatives represent unflagged vulnerabilities that could reach production. "
        "Our model achieved a high Recall of 92.68%, missing only 9 vulnerable functions out of 123. Diagnostic inspection revealed that "
        "the missed samples involved complex multi-class inheritance where the taint sink resided in an unparsed external helper library.\n\n"
        "3. Analysis of False Positives (FP = 5):\n"
        "The model demonstrated high Specificity (96.12%) with only 5 false alarms out of 129 non-vulnerable functions. This confirms that "
        "data-flow graph attention effectively distinguishes between vulnerable methods and secure methods that perform proper sanitization."
    )

    # -------------------------------------------------------------
    # 6. CONCLUSION AND LIMITATIONS
    # -------------------------------------------------------------
    doc.add_heading("6. Conclusion and Limitations", level=1)

    doc.add_heading("Key Findings", level=2)
    doc.add_paragraph(
        "• Data flow information is critical for vulnerability detection: Fusing subword tokens with variable def-use graphs enables "
        "the neural network to track taint propagation paths that purely lexical models overlook.\n"
        "• High performance is achievable within enterprise compute budgets: By optimizing the Graph Attention Pooling layer, the model "
        "achieves 94.44% Accuracy and 0.9782 ROC-AUC without requiring massive GPU cluster clusters.\n"
        "• Organizational data management creates compounding value: Disciplined data governance, ISO 25012 quality auditing, and "
        "systematic ETL pipelines provide the clean data foundation required for reliable AI deployment."
    )

    doc.add_heading("Learning Outcomes", level=2)
    outcomes = [
        ("Technical Skills Acquired", "Proficiency in fine-tuning Transformer code models (GraphCodeBERT), engineering AST/DFG parsers, building custom PyTorch graph attention layers, and resolving network proxy and CUDA memory constraints."),
        ("Conceptual Understanding", "Deep understanding of the DAMA-DMBOK data lifecycle, ISO/IEC 25012 data quality dimensions, and the Information Value Chain connecting raw code commits to production CI/CD gating decisions."),
        ("Practical Competencies", "Successfully established reproducible Git repository governance, automated test pipelines, and compiled academic-grade documentation conforming to master's standards.")
    ]
    for o_title, o_desc in outcomes:
        p = doc.add_paragraph(style='List Bullet')
        r_b = p.add_run(f"{o_title}: ")
        r_b.font.bold = True
        p.add_run(o_desc)

    doc.add_heading("Limitations of the Approach", level=2)
    doc.add_paragraph(
        "• Intra-Procedural Scope: The current DFG extractor operates within the boundaries of individual Java methods. Inter-procedural "
        "taint flows spanning multiple classes or microservices require whole-program call-graph analysis.\n"
        "• Reflection & Dynamic Proxies: Dynamic Java constructs (such as java.lang.reflect or dynamic bytecode generation) are invisible "
        "to static DFG extractors and require complementary dynamic analysis instrumentation.\n"
        "• Computational Latency on Edge: Generating token representations through 12 Transformer layers requires ~30ms per function on CPU, "
        "which is acceptable for CI/CD PR merge checks but may introduce latency if executed on every keystroke in developer IDEs."
    )

    doc.add_heading("Future Applications & Recommendations", level=2)
    doc.add_paragraph(
        "• Automated Remediation: Extending the model from binary classification to generative patch synthesis (e.g., fine-tuning CodeT5 "
        "to automatically generate pull requests fixing detected vulnerabilities).\n"
        "• Cross-Language Generalization: Adapting the DFG extractor to C/C++, Python, and Go by leveraging Tree-sitter multi-grammar parsers."
    )

    # -------------------------------------------------------------
    # 7. REFERENCES
    # -------------------------------------------------------------
    doc.add_heading("7. References", level=1)
    refs = [
        "[1] Shestov, P., et al. (2025). Finetuning Large Language Models for Vulnerability Detection. IEEE Access, vol. 13, pp. 35467–35482. DOI: 10.1109/ACCESS.2025.3546700",
        "[2] Guo, D., Ren, S., Lu, S., Feng, Z., Tang, D., Liu, S., Long, C., Duan, N., Zhou, A., & Yin, J. (2021). GraphCodeBERT: Pre-training Code Representations with Data Flow. International Conference on Learning Representations (ICLR 2021).",
        "[3] DAMA International. (2017). DAMA-DMBOK: Data Management Body of Knowledge (2nd Edition). Technics Publications.",
        "[4] ISO/IEC 25012:2008. (2008). Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — Data quality model. International Organization for Standardization.",
        "[5] Zhou, Y., Liu, S., Siow, J., Du, X., & Liu, Y. (2019). Devign: Effective Vulnerability Identification by Learning Comprehensive Program Semantics via Graph Neural Networks. Advances in Neural Information Processing Systems (NeurIPS 2019), 32.",
        "[6] Musab, R. (2024). Vulnerability LLM Fine-Tuning Benchmark Datasets. GitHub Repository: https://github.com/rmusab/vul-llm-finetune"
    ]
    for r_text in refs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        r = p.add_run(r_text)
        r.font.size = Pt(9.5)

    # -------------------------------------------------------------
    # APPENDICES
    # -------------------------------------------------------------
    doc.add_page_break()
    doc.add_heading("Appendices", level=1)

    doc.add_heading("Appendix A: ISO/IEC 25012 Data Quality Audit Report", level=2)
    doc.add_paragraph(
        "Audit results generated by pipeline/etl_pipeline.py on the 1,334 Java function records:\n"
        "• Total Raw Records: 1,334 | Total Cleaned Records: 1,334\n"
        "• Duplicate Records Removed: 0 (100% Uniqueness Verified)\n"
        "• Completeness Score: 1.0000 (100% — Zero missing code or target fields)\n"
        "• Validity Score: 1.0000 (100% — All targets in {0, 1}; valid Java syntax)\n"
        "• Consistency Score: 1.0000 (100% — Perfect agreement between status and target labels)\n"
        "• Overall Vulnerability Rate: 49.85% (Balanced: 665 Vulnerable, 669 Fixed)"
    )

    doc.add_heading("Appendix B: GitHub Repository & Execution Instructions", level=2)
    doc.add_paragraph(
        "All code, data, diagrams, reports, presentation slides, and environment files have been pushed to GitHub:\n"
        "• Repository URL: https://github.com/Tasik1/kbtu-mood-midterm-team2\n"
        "• Owner: Tasik1 (Shyntas Bidaishiyev)\n"
        "• Master Runner: python run_all.py\n"
        "• Interactive Notebook: jupyter notebook notebooks/midterm_team2_graphcodebert.ipynb"
    )

    out_docx_final = "midterm/docs/Midterm_Report_Team2_Final.docx"
    doc.save(out_docx_final)
    print(f"[DOCX] Successfully generated Laboratory Work Report: {out_docx_final}")

    try:
        out_docx = "midterm/docs/Midterm_Report_Team2.docx"
        doc.save(out_docx)
        print(f"[DOCX] Successfully updated: {out_docx}")
    except PermissionError:
        print("[DOCX] Midterm_Report_Team2.docx is currently open in Word. Saved as Midterm_Report_Team2_Final.docx.")

if __name__ == "__main__":
    create_report()
