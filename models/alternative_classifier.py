"""
Alternative Method: GraphCodeBERT + Frozen Embeddings + Random Forest Classifier.
Course: Management of Organizational Data (MoOD) 2026 - Master's Programme
Team 2: Bidaishiev Shyntas, Ibragim Anzir, Ardak Aruzhan, Amanbayev Farkhad

Serves as the baseline/alternative under syllabus guidelines when evaluating
computational trade-offs, inference latency, and organizational resource constraints.
"""

import numpy as np
from typing import Dict, Any, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import joblib

class GraphCodeBERTRandomForest:
    def __init__(
        self,
        n_estimators: int = 300,
        max_depth: int = 18,
        min_samples_split: int = 4,
        min_samples_leaf: int = 2,
        random_state: int = 42
    ):
        self.rf = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            class_weight="balanced",
            n_jobs=-1,
            random_state=random_state
        )
        self.is_fitted = False

    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> "GraphCodeBERTRandomForest":
        self.rf.fit(X_train, y_train)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before predict.")
        return self.rf.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before predict_proba.")
        return self.rf.predict_proba(X)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        preds = self.predict(X_test)
        probs = self.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, zero_division=0)
        rec = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)
        roc_auc = roc_auc_score(y_test, probs)
        cm = confusion_matrix(y_test, preds).tolist()

        return {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
            "confusion_matrix": cm,
            "predictions": preds.tolist(),
            "probabilities": probs.tolist()
        }

    def save(self, filepath: str):
        joblib.dump(self.rf, filepath)

    def load(self, filepath: str):
        self.rf = joblib.load(filepath)
        self.is_fitted = True
