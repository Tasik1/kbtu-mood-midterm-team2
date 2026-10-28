"""
ETL & Data Quality Pipeline for Java Vulnerability Detection.
Course: Management of Organizational Data (MoOD) 2026 - Master's Programme
Team 2: Bidaishiev Shyntas, Ibragim Anzir, Ardak Aruzhan, Amanbayev Farkhad

Covers:
- Lecture 1: Organizational Data Lifecycle (Acquisition -> Validation -> Storage -> Transformation)
- Lecture 4: Data Warehousing and ETL Processing
- Lecture 5: Data Quality Assessment (Completeness, Uniqueness, Validity, Consistency)
"""

import os
import json
import re
import hashlib
from collections import Counter
from typing import Dict, List, Tuple, Any

class JavaVulnerabilityETL:
    def __init__(self, raw_dir: str = None, processed_dir: str = None):
        self.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.raw_dir = raw_dir or os.path.join(self.repo_root, "data", "extracted")
        self.processed_dir = processed_dir or os.path.join(self.repo_root, "data", "processed")
        os.makedirs(self.processed_dir, exist_ok=True)
        self.quality_metrics: Dict[str, Any] = {}

    @staticmethod
    def clean_java_code(code: str) -> str:
        """
        Cleans and normalizes Java source code:
        - Replaces carriage returns
        - Strips trailing whitespaces per line
        - Removes consecutive empty lines
        """
        if not code:
            return ""
        code = code.replace("\r\n", "\n").replace("\r", "\n")
        lines = [line.rstrip() for line in code.split("\n")]
        # collapse more than 2 consecutive blank lines
        cleaned_lines = []
        blank_count = 0
        for line in lines:
            if not line.strip():
                blank_count += 1
                if blank_count <= 2:
                    cleaned_lines.append("")
            else:
                blank_count = 0
                cleaned_lines.append(line)
        return "\n".join(cleaned_lines).strip()

    @staticmethod
    def compute_sha256(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def run_etl(self) -> Dict[str, Any]:
        """
        Executes complete ETL pipeline across train, valid, and test splits.
        """
        splits = ["train", "valid", "test"]
        summary = {
            "splits": {},
            "overall": {
                "total_raw_records": 0,
                "total_cleaned_records": 0,
                "duplicates_removed": 0,
                "overall_completeness": 1.0,
                "overall_validity": 1.0,
                "class_balance_ratio": {}
            }
        }

        all_seen_hashes = set()

        for split in splits:
            raw_path = os.path.join(self.raw_dir, f"{split}.jsonl")
            if not os.path.exists(raw_path):
                raise FileNotFoundError(f"Source file not found: {raw_path}")

            raw_records = []
            with open(raw_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        raw_records.append(json.loads(line.strip()))

            total_raw = len(raw_records)
            cleaned_records = []
            seen_in_split = set()
            duplicates_in_split = 0
            null_fields_count = 0
            invalid_targets = 0
            cwes = []
            targets = []
            code_lengths = []

            for rec in raw_records:
                # 1. Validation of required fields
                code = rec.get("code", "")
                target = rec.get("target")
                idx = rec.get("idx")

                if code is None or target is None or idx is None:
                    null_fields_count += 1
                    continue

                if target not in (0, 1):
                    invalid_targets += 1
                    continue

                cleaned_code = self.clean_java_code(code)
                if len(cleaned_code) < 10:
                    null_fields_count += 1
                    continue

                code_hash = self.compute_sha256(cleaned_code)
                if code_hash in seen_in_split:
                    duplicates_in_split += 1
                    continue
                seen_in_split.add(code_hash)
                all_seen_hashes.add(code_hash)

                # Consistent normalization
                clean_rec = {
                    "idx": idx,
                    "target": int(target),
                    "cwe": rec.get("cwe", "Unknown"),
                    "function_name": rec.get("function_name", "unknown_function"),
                    "commit": rec.get("commit", ""),
                    "status": rec.get("status", "VULNERABLE" if target == 1 else "FIXED"),
                    "code": cleaned_code,
                    "code_hash": code_hash,
                    "token_count": len(cleaned_code.split()),
                    "line_count": len(cleaned_code.split("\n"))
                }

                cleaned_records.append(clean_rec)
                cwes.append(clean_rec["cwe"])
                targets.append(clean_rec["target"])
                code_lengths.append(clean_rec["token_count"])

            # Save cleaned jsonl
            out_path = os.path.join(self.processed_dir, f"{split}_cleaned.jsonl")
            with open(out_path, "w", encoding="utf-8") as out_f:
                for cr in cleaned_records:
                    out_f.write(json.dumps(cr) + "\n")

            target_counts = dict(Counter(targets))
            cwe_counts = dict(Counter(cwes).most_common(10))

            split_metric = {
                "raw_count": total_raw,
                "cleaned_count": len(cleaned_records),
                "duplicates_removed": duplicates_in_split,
                "completeness_score": round((total_raw - null_fields_count) / total_raw, 4),
                "validity_score": round((total_raw - invalid_targets) / total_raw, 4),
                "uniqueness_score": round(len(cleaned_records) / total_raw, 4),
                "class_distribution": {
                    "0_non_vulnerable": target_counts.get(0, 0),
                    "1_vulnerable": target_counts.get(1, 0)
                },
                "vulnerability_rate": round(target_counts.get(1, 0) / max(1, len(cleaned_records)), 4),
                "top_cwes": cwe_counts,
                "avg_token_count": round(sum(code_lengths) / max(1, len(code_lengths)), 2),
                "max_token_count": max(code_lengths) if code_lengths else 0,
                "min_token_count": min(code_lengths) if code_lengths else 0
            }
            summary["splits"][split] = split_metric
            summary["overall"]["total_raw_records"] += total_raw
            summary["overall"]["total_cleaned_records"] += len(cleaned_records)
            summary["overall"]["duplicates_removed"] += duplicates_in_split

        # Overall rates
        total_clean = summary["overall"]["total_cleaned_records"]
        total_vuln = sum(summary["splits"][s]["class_distribution"]["1_vulnerable"] for s in splits)
        summary["overall"]["overall_vulnerability_rate"] = round(total_vuln / max(1, total_clean), 4)

        report_path = os.path.join(self.repo_root, "results", "data_quality_report.json")
        with open(report_path, "w", encoding="utf-8") as rf:
            json.dump(summary, rf, indent=2)

        self.quality_metrics = summary
        print(f"[ETL] Completed. Total processed: {total_clean} records. Quality report saved to {report_path}")
        return summary

if __name__ == "__main__":
    etl = JavaVulnerabilityETL()
    metrics = etl.run_etl()
    print(json.dumps(metrics, indent=2))
