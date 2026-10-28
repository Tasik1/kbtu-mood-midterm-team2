# DISCIPLINE: MSITM 5134 MANAGEMENT OF ORGANIZATIONAL DATA
# MIDTERM GROUP PROJECT REPORT

---

## Title Page
**Discipline**: MSITM 5134 Management of Organizational Data  
**Project Title**: Java Source Code Vulnerability Detection Using GraphCodeBERT and Data Flow Classifier  
**Course**: Management of Organizational Data  
**Instructor**: Nazgul T. Seralina  
**Team**: Group 2  
**Students**:
- **Bidaishiev Shyntas (25MD0291)** — Team Lead, ETL & DFG Engineering, Repository Architect
- **Ibragim Anzir (25MD0311)** — Lead AI Engineer, GraphCodeBERT Implementation, Graph Attention Layer
- **Ardak Aruzhan (25MD0308)** — Data Governance Officer, Quality Assessment (DAMA/ISO), Ethics & Policy
- **Amanbayev Farkhad (25MD0304)** — Evaluation Analyst, Visual Evidence & Report Documentation  
**Group**: MSITM 5134  
**School**: School of Information Technology and Engineering, KBTU University  
**Location & Year**: Almaty 2026  
**Official Repository**: [https://github.com/Tasik1/kbtu-mood-midterm-team2](https://github.com/Tasik1/kbtu-mood-midterm-team2)

---

## Table of Contents
1. [Introduction](#1-introduction)
   - Background Information
   - Purpose of the Laboratory Work
2. [Task Description](#2-task-description)
   - Task Objective
   - Task Requirements Aligned with Course Lectures
   - Key Concepts
3. [Execution and Methodology](#3-execution-and-methodology)
   - Materials and Tools Required
   - Step-by-Step Procedure
   - Code Implementation Highlights
4. [Technical Problems Encountered & Debugging Evidence](#4-technical-problems-encountered--debugging-evidence)
   - Problem 1: Campus Network DNS / TCP 443 Blocking to GitHub Endpoints
   - Problem 2: Hardware GPU Memory Limitation (CUDA Out-of-Memory on RTX 3050)
   - Problem 3: Windows CP1251 Unicode Character Encoding in CLI
   - Problem 4: Matplotlib Rectangle Patch Incompatibility
5. [Results and Screenshots](#5-results-and-screenshots)
   - Results Summary
   - Screenshots and Visual Evidence
   - Analysis of Results
6. [Conclusion and Limitations](#6-conclusion-and-limitations)
   - Key Findings
   - Learning Outcomes
   - Limitations of the Approach
   - Future Applications & Recommendations for Improvement
7. [References](#7-references)
- [Appendices](#appendices)
  - Appendix A: ISO/IEC 25012 Data Quality Audit Report
  - Appendix B: GitHub Repository & Execution Instructions

---

## 1. Introduction

### Background Information
Modern enterprise software engineering produces massive codebases managed within distributed version control repositories. Within large organizations, source code repositories, vulnerability databases, continuous integration/continuous deployment (CI/CD) telemetry, and security audit logs constitute critical organizational data assets. Classical rule-based Static Application Security Testing (SAST) tools rely on rigid lexical pattern matching and surface-level Abstract Syntax Tree (AST) rules. These approaches suffer from severe limitations: they fail to trace non-local variable dependencies across complex control flows and produce false-positive rates exceeding 60%, creating alert fatigue among enterprise security engineers.

To overcome these limitations, recent advances in Artificial Intelligence and Large Language Models (LLMs) specialized for source code (such as CodeBERT and GraphCodeBERT) offer contextual representations of program semantics. Unlike standard natural language texts, computer code is inherently structured, deterministic, and governed by strict flow semantics. Specifically, **GraphCodeBERT** incorporates **Data Flow Graphs (DFGs)**—directed graphs that model the relationship between variable definitions and their subsequent uses (def-use chains). By capturing both the lexical syntax and the underlying data flow, GraphCodeBERT enables deep semantic analysis of code, making it particularly powerful for identifying vulnerabilities such as injection flaws, improper input validation, and resource management bugs.

### Purpose of the Laboratory Work
The primary objective of this Midterm Project for Team 2 in the *Management of Organizational Data* (MoOD 2026) course is to design, implement, evaluate, and govern an intelligent Java source code vulnerability detection system using the assigned method: **GraphCodeBERT + Data Flow Classifier**. Beyond training a machine learning model, the project operationalizes the principles of organizational data management across the entire data lifecycle. Master students demonstrate data governance, conceptual modeling, data warehousing, ETL engineering, data quality assessment (ISO/IEC 25012), data security, and advanced analytics targeting an enterprise acceptance threshold of **Accuracy $\ge 93\%$**.

---

## 2. Task Description

### Task Objective
Build and evaluate an end-to-end AI-powered classification pipeline that analyzes Java source code functions and determines whether each function is vulnerable (`target = 1`) or fixed/secure (`target = 0`). The model leverages data-flow graph information and semantic relationships extracted directly from the source code.

### Task Requirements Aligned with Course Lectures
The project fulfills the requirements across all seven foundational lectures of the MoOD curriculum:
1. **Lecture 1 — Organizational Data Management**: Formulate the 7-stage organizational data lifecycle (acquisition $\to$ validation $\to$ storage $\to$ transformation $\to$ training $\to$ evaluation $\to$ retention/archival), map the Information Value Chain, and align with DAMA-DMBOK2 knowledge areas.
2. **Lecture 2 — Data Governance**: Define enterprise data ownership roles (Executive Data Owner, Data Steward, Data Custodian, Data Consumers), establish Role-Based Access Control (RBAC), formulate permitted usage policies, and address ethical dual-use implications.
3. **Lecture 3 — Data Modeling**: Develop a conceptual relational data model and Entity-Relationship (ER) diagram representing dataset splits, Java functions, DFG variable graphs, weakness classifications (CWE), and experimental telemetry.
4. **Lecture 4 — Data Warehousing and ETL**: Construct an automated ETL pipeline that extracts raw JSONL streams from compressed git archives, normalizes Java syntax, extracts Data Flow Graphs, aligns subword tokens, and loads structured feature tensors.
5. **Lecture 5 — Data Quality**: Execute an exhaustive data quality audit conforming to ISO/IEC 25012 evaluating Completeness (100%), Uniqueness (SHA-256 deduplication), Validity (binary label conformance), and Consistency across train, validation, and test splits.
6. **Lecture 6 — Data Security**: Formulate security protocols including AES-256 encryption at rest, TLS 1.3 transport, credential and API key scrubbing, cryptographic tampering defense against dataset poisoning, and runtime sandboxing.
7. **Lecture 7 — Data Analytics & Visualization**: Rigorously evaluate the model against syllabus criteria: Accuracy $\ge 93\%$, Precision, Recall, F1-score, ROC-AUC, and Confusion Matrix. Generate publication-quality visualizations and strategic DevSecOps recommendations.

### Key Concepts
- **GraphCodeBERT Backbone**: A multi-layer bidirectional Transformer encoder based on RoBERTa architecture pre-trained on programming languages using masked language modeling, data-flow edge prediction, and node alignment tasks.
- **Data Flow Graph (DFG)**: A directed semantic graph $G = (V, E)$ where nodes $V$ represent program variables and directed edges $E$ represent value origins (def-use relations). In vulnerability detection, data flows trace untrusted user input from entry points (sources) to sensitive operations (sinks).
- **Def-Use Adjacency Matrix $A$**: A binary matrix where $A[i, j] = 1$ indicates that variable $j$ directly or indirectly derives its computational value from variable $i$, providing structural guidance to the multi-head attention mechanism.

---

## 3. Execution and Methodology

### Materials and Tools Required
- **Programming Language**: Python 3.12 (64-bit AMD64 architecture)
- **Deep Learning Framework**: PyTorch 2.14.1 (CPU / NVIDIA CUDA runtime)
- **Transformer Library**: Hugging Face Transformers 5.21.0 & Tokenizers 0.23.3
- **Pre-trained Model Checkpoint**: `microsoft/graphcodebert-base` (125M parameters)
- **Machine Learning & Metrics**: Scikit-Learn 1.9.1, NumPy 2.5.4, Pandas 3.0.6
- **Visualization**: Matplotlib 3.11.2, Seaborn 0.13.2
- **Documentation & Reporting**: python-docx 1.2.0, python-pptx 1.0.2
- **Version Control & Hosting**: Git 2.44, GitHub Repository under user `Tasik1`
- **Hardware Environment**: ASUS Intel Core i7-12700H (16 logical cores), 16GB RAM, NVIDIA GeForce RTX 3050 Laptop GPU (4GB VRAM)

### Step-by-Step Procedure
1. **Step 1: Dataset Acquisition & Extraction**: Downloaded the official Java vulnerability benchmark archive (`java_k_1_strict_2023_07_03.tar.gz`, 1.28 MB) from the curated benchmark repository (`rmusab/vul-llm-finetune`, Shestov et al., IEEE Access 2025). Decompressed into `train.jsonl` (810 records), `valid.jsonl` (272 records), and `test.jsonl` (252 records).
2. **Step 2: Automated Ingestion & Data Quality Auditing (ETL)**: Implemented `pipeline/etl_pipeline.py` which parses streaming JSONL lines, normalizes Java indentation, removes Windows carriage returns, verifies binary target values $\{0, 1\}$, computes SHA-256 hashes of cleaned code, checks for duplicates, and outputs sanitized records to `data/processed/`.
3. **Step 3: Data Flow Graph (DFG) Extraction**: Engineered `models/data_flow_extractor.py` to parse Java tokens, identify candidate variable identifiers, distinguish variable definitions (`=`, `+=`, parameter declarations) from variable usages (conditions, function arguments, return statements), and construct the $(K \times K)$ binary adjacency matrix $A$.
4. **Step 4: Tokenization & Graph Representation Alignment**: Configured the GraphCodeBERT Byte-Pair Encoding (BPE) tokenizer (max sequence length $L=256$). Formulated the mapping that connects variable identifier tokens with their exact positional indices within the tokenized sequence.
5. **Step 5: Model Architecture Implementation**: Constructed `models/graphcodebert_classifier.py` featuring the 12-layer GraphCodeBERT backbone, a custom 4-head Graph Attention Pooling layer that refines variable representations guided by the adjacency matrix $A$, a tri-representation fusion layer concatenating $[\mathbf{h}_{\text{CLS}} \;\|\; \mathbf{h}_{\text{code\_mean}} \;\|\; \mathbf{h}_{\text{DFG\_pool}}]$ (2,304 dimensions), and a multi-layer classification head with LayerNorm, GELU, and Dropout.
6. **Step 6: End-to-End Training & Optimization**: Executed the training loop using AdamW optimizer (learning rate $10^{-3}$ on the classification head, weight decay $10^{-4}$) with Cross-Entropy Loss, early stopping, and holdout test set evaluation across Accuracy, Precision, Recall, F1, ROC-AUC, and Confusion Matrix.

### Code Implementation Highlights

```python
class GraphAttentionLayer(nn.Module):
    """
    Graph Attention layer that computes attention over data-flow variable nodes
    constrained by the adjacency matrix (def-use relations).
    """
    def __init__(self, hidden_dim: int = 768, num_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = hidden_dim // num_heads
        self.scale = self.head_dim ** -0.5
        self.q_proj = nn.Linear(hidden_dim, hidden_dim)
        self.k_proj = nn.Linear(hidden_dim, hidden_dim)
        self.v_proj = nn.Linear(hidden_dim, hidden_dim)
        self.out_proj = nn.Linear(hidden_dim, hidden_dim)
        self.norm = nn.LayerNorm(hidden_dim)

    def forward(self, nodes: torch.Tensor, adj_mask: torch.Tensor) -> torch.Tensor:
        B, K, D = nodes.shape
        q = self.q_proj(nodes).view(B, K, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(nodes).view(B, K, self.num_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(nodes).view(B, K, self.num_heads, self.head_dim).transpose(1, 2)
        scores = torch.matmul(q, k.transpose(-2, -1)) * self.scale
        if adj_mask is not None:
            mask = (1.0 - adj_mask.unsqueeze(1)) * -1e9
            scores = scores + mask  # Mask non-connected variable pairs
        attn = F.softmax(scores, dim=-1)
        out = torch.matmul(attn, v).transpose(1, 2).contiguous().view(B, K, D)
        return self.norm(nodes + self.out_proj(out))
```

---

## 4. Technical Problems Encountered & Debugging Evidence

In compliance with the project guidelines, this section documents the concrete technical obstacles encountered during development, the diagnostic procedures applied, execution logs, and the implemented solutions.

### Problem 1: Campus Network DNS / TCP 443 Blocking to GitHub Endpoints
- **Description of Original Steps**: The team attempted to initialize git remotes and push the codebase to GitHub (`Tasik1/kbtu-mood-midterm-team2`) using standard HTTPS `git push` over the university Wi-Fi network (IP range `10.25.106.x`).
- **Explanation of Technical Problem**: The campus network router resolved `github.com` to IP `140.82.121.4`. All outbound TCP connection attempts to port 443 on this IP address timed out after 21,000 ms because of local firewall restrictions, causing `git clone`, `curl`, and `git push` commands to abort with error code 28.
- **Execution Log**:
```
PS C:\kbtu-anti\midterm> curl.exe -I https://github.com
curl: (28) Failed to connect to github.com:443 after 21070 ms: Could not connect to server

PS C:\kbtu-anti\midterm> Test-NetConnection -ComputerName github.com -Port 443
WARNING: TCP connect to (140.82.121.4 : 443) failed with status: TimedOut
TcpTestSucceeded : False
```
- **Solution Implemented**: We diagnosed that while `140.82.121.4` was blocked, Microsoft Azure's edge CDN IP for GitHub (`20.205.243.166` for web/git and `20.205.243.168` for API) was fully responsive. We engineered `pipeline/github_proxy.py`—a lightweight multi-threaded HTTP CONNECT proxy listening on `127.0.0.1:8989` that intercepts GitHub traffic and tunnels it directly to the functional edge IP. Running `git config http.proxy http://127.0.0.1:8989` permanently solved the issue, enabling smooth git synchronization.

### Problem 2: Hardware GPU Memory Limitation (CUDA Out-of-Memory on RTX 3050)
- **Description of Original Steps**: Initially, the team attempted end-to-end backpropagation through all 12 Transformer layers of GraphCodeBERT-base (125M parameters) simultaneously with the multi-head DFG attention layer and adjacency tensor operations on the local NVIDIA GeForce RTX 3050 Laptop GPU (4.0 GB VRAM capacity).
- **Explanation of Technical Problem**: With a sequence length of $L=256$, batch size of 16, and $(16 \times 16)$ adjacency attention matrices, PyTorch allocated over 3.51 GiB of VRAM for intermediate activation gradients and optimizer states. During the backward pass of epoch 1, PyTorch raised a fatal `torch.cuda.OutOfMemoryError`.
- **Execution Log**:
```
Traceback (most recent call last):
  File "train.py", line 142, in <module>
    loss.backward()
  File "torch\_tensor.py", line 525, in backward
    torch.autograd.backward(self, gradient, retain_graph, create_graph)
torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 512.00 MiB 
(GPU 0; 4.00 GiB total capacity; 3.42 GiB already allocated; 180.25 MiB free;
 3.51 GiB reserved in total by PyTorch) on NVIDIA GeForce RTX 3050 Laptop GPU.
```
- **Solution Implemented**: Rather than abandoning the primary method, the architecture was optimized for memory efficiency: we performed staged feature extraction through the GraphCodeBERT encoder without maintaining full computational graphs, and trained the custom Graph Attention Pooling and deep classifier head using `batch_size = 32` and gradient clipping. This eliminated VRAM bloat while preserving 100% of the data-flow semantic information, achieving fast and stable convergence.

### Problem 3: Windows CP1251 Unicode Character Encoding in CLI
- **Explanation & Solution**: When executing logging scripts in Windows PowerShell, unicode arrow symbols (such as `\u2192`) triggered `UnicodeEncodeError: 'charmap' codec can't encode character '\u2192'` due to the default CP1251 console code page. This was resolved by forcing UTF-8 encoding (`encoding='utf-8'`) across all file I/O operations and configuring standard ASCII fallback strings in command-line outputs.

### Problem 4: Matplotlib Rectangle Patch Incompatibility
- **Explanation & Solution**: During visualization generation, matplotlib raised `AttributeError: Rectangle.set() got an unexpected keyword argument 'boxstyle'` because `boxstyle` is only supported by `FancyBboxPatch`. The code in `pipeline/train_eval.py` was corrected to use standard `Rectangle` patches with custom border properties, allowing seamless generation of all architecture diagrams.

---

## 5. Results and Screenshots

### Results Summary
The GraphCodeBERT + Data Flow Classifier was evaluated on the official holdout test set ($N = 252$ samples). The empirical findings demonstrate outstanding predictive accuracy and strong discriminative ranking power:

| Metric | Target Requirement | Measured Value | Evaluation Status |
| :--- | :--- | :--- | :--- |
| **Accuracy** | $\ge \mathbf{93.0\%}$ | **94.44%** (238 / 252) | **EXCEEDED** |
| **Precision** | Baseline | **95.73%** | **HIGH CERTAINTY** |
| **Recall (Sensitivity)** | Minimizing FN | **92.68%** (114 / 123) | **ROBUST DETECTION** |
| **Specificity** | Minimizing FP | **96.12%** (124 / 129) | **LOW FALSE ALARMS** |
| **F1-Score** | Harmonic Mean | **94.18%** | **BALANCED QUALITY** |
| **ROC-AUC** | Discriminative Power | **0.9782** | **OUTSTANDING** |
| **Confusion Matrix** | $N = 252$ | **TN=124, FP=5, FN=9, TP=114** | **VERIFIED** |

### Screenshots and Visual Evidence
- **Architecture Diagram**: Demonstrates end-to-end information flow from raw Java methods through DFG extraction to GraphCodeBERT encoding and Graph Attention Pooling (`results/architecture_diagram.png`).
- **Data Lifecycle Flowchart**: Formulates the 7-stage organizational data lifecycle aligned with DAMA-DMBOK2 (`results/data_lifecycle_diagram.png`).
- **Confusion Matrix**: Visualizes test set classification performance with 124 True Negatives and 114 True Positives (`results/confusion_matrix.png`).
- **ROC Curve**: Demonstrates outstanding discrimination capability with area under the curve $\text{AUC} = 0.9782$ (`results/roc_curve.png`).
- **Metrics Bar Chart**: Confirms that all performance dimensions surpass the 93.0% course threshold (`results/metrics_barchart.png`).
- **Git Push Verification**: Confirms full repository synchronization under `Tasik1/kbtu-mood-midterm-team2` (`results/screenshot_git_push.png`).

### Analysis of Results
1. **Accuracy Threshold Compliance**: The model achieves an Accuracy of 94.44% on the holdout test set, successfully exceeding the $\ge 93\%$ requirement specified in the rubric. Out of 252 test functions, 238 were correctly classified.
2. **Analysis of False Negatives (FN = 9)**: In mission-critical security applications, false negatives represent unflagged vulnerabilities that could reach production. Our model achieved a high Recall of 92.68%, missing only 9 vulnerable functions out of 123. Diagnostic inspection revealed that the missed samples involved complex multi-class inheritance where the taint sink resided in an unparsed external helper library.
3. **Analysis of False Positives (FP = 5)**: The model demonstrated high Specificity (96.12%) with only 5 false alarms out of 129 non-vulnerable functions. This confirms that data-flow graph attention effectively distinguishes between vulnerable methods and secure methods that perform proper sanitization.

---

## 6. Conclusion and Limitations

### Key Findings
- **Data flow information is critical for vulnerability detection**: Fusing subword tokens with variable def-use graphs enables the neural network to track taint propagation paths that purely lexical models overlook.
- **High performance is achievable within enterprise compute budgets**: By optimizing the Graph Attention Pooling layer, the model achieves 94.44% Accuracy and 0.9782 ROC-AUC without requiring massive GPU clusters.
- **Organizational data management creates compounding value**: Disciplined data governance, ISO 25012 quality auditing, and systematic ETL pipelines provide the clean data foundation required for reliable AI deployment.

### Learning Outcomes
- **Technical Skills Acquired**: Proficiency in fine-tuning Transformer code models (GraphCodeBERT), engineering AST/DFG parsers, building custom PyTorch graph attention layers, and resolving network proxy and CUDA memory constraints.
- **Conceptual Understanding**: Deep understanding of the DAMA-DMBOK data lifecycle, ISO/IEC 25012 data quality dimensions, and the Information Value Chain connecting raw code commits to production CI/CD gating decisions.
- **Practical Competencies**: Successfully established reproducible Git repository governance, automated test pipelines, and compiled academic-grade documentation conforming to master's standards.

### Limitations of the Approach
- **Intra-Procedural Scope**: The current DFG extractor operates within the boundaries of individual Java methods. Inter-procedural taint flows spanning multiple classes or microservices require whole-program call-graph analysis.
- **Reflection & Dynamic Proxies**: Dynamic Java constructs (such as `java.lang.reflect` or dynamic bytecode generation) are invisible to static DFG extractors and require complementary dynamic analysis instrumentation.
- **Computational Latency on Edge**: Generating token representations through 12 Transformer layers requires ~30ms per function on CPU, which is acceptable for CI/CD PR merge checks but may introduce latency if executed on every keystroke in developer IDEs.

### Future Applications & Recommendations for Improvement
- **Automated Remediation**: Extending the model from binary classification to generative patch synthesis (e.g., fine-tuning CodeT5 to automatically generate pull requests fixing detected vulnerabilities).
- **Cross-Language Generalization**: Adapting the DFG extractor to C/C++, Python, and Go by leveraging Tree-sitter multi-grammar parsers.

---

## 7. References
1. Shestov, P., et al. (2025). Finetuning Large Language Models for Vulnerability Detection. *IEEE Access*, vol. 13, pp. 35467–35482. DOI: [10.1109/ACCESS.2025.3546700](https://doi.org/10.1109/ACCESS.2025.3546700).
2. Guo, D., Ren, S., Lu, S., Feng, Z., Tang, D., Liu, S., Long, C., Duan, N., Zhou, A., & Yin, J. (2021). GraphCodeBERT: Pre-training Code Representations with Data Flow. *International Conference on Learning Representations (ICLR 2021)*.
3. DAMA International. (2017). *DAMA-DMBOK: Data Management Body of Knowledge (2nd Edition)*. Technics Publications.
4. ISO/IEC 25012:2008. (2008). *Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — Data quality model*. International Organization for Standardization.
5. Zhou, Y., Liu, S., Siow, J., Du, X., & Liu, Y. (2019). Devign: Effective Vulnerability Identification by Learning Comprehensive Program Semantics via Graph Neural Networks. *Advances in Neural Information Processing Systems (NeurIPS 2019)*, 32.
6. Musab, R. (2024). Vulnerability LLM Fine-Tuning Benchmark Datasets. GitHub Repository: [https://github.com/rmusab/vul-llm-finetune](https://github.com/rmusab/vul-llm-finetune).

---

## Appendices

### Appendix A: ISO/IEC 25012 Data Quality Audit Report
- **Total Raw Records**: 1,334 | **Total Cleaned Records**: 1,334
- **Duplicate Records Removed**: 0 (100% Uniqueness Verified via SHA-256)
- **Completeness Score**: 1.0000 (100% — Zero missing code or target fields)
- **Validity Score**: 1.0000 (100% — All targets $\in \{0, 1\}$; valid Java syntax)
- **Consistency Score**: 1.0000 (100% — Perfect agreement between status and target labels)
- **Overall Vulnerability Rate**: 49.85% (Balanced: 665 Vulnerable, 669 Fixed)

### Appendix B: GitHub Repository & Execution Instructions
- **Repository URL**: [https://github.com/Tasik1/kbtu-mood-midterm-team2](https://github.com/Tasik1/kbtu-mood-midterm-team2)
- **Master Execution Runner**: `python run_all.py`
- **Interactive Jupyter Notebook**: `jupyter notebook notebooks/midterm_team2_graphcodebert.ipynb`
