"""
PhishGuard AI – Model Training Script
======================================
Trains a Random Forest classifier on URL-level features extracted from a
labelled phishing/legitimate dataset.

Usage
-----
    python train.py --dataset datasets/phishing_dataset.csv \
                    --output  models/phishguard_model.joblib \
                    --test-size 0.2

Dataset format (CSV)
--------------------
The script expects a CSV file with at least the columns:
    url   (str)  – the raw URL
    label (int)  – 1 = phishing, 0 = legitimate
"""

from __future__ import annotations

import argparse
import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Ensure the backend detectors are importable when run from this directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
from detectors.url_analyzer import URLAnalyzer  # noqa: E402


# ── Feature extraction ────────────────────────────────────────────────────────

URL_FEATURES = [
    "url_length",
    "num_dots",
    "num_hyphens",
    "num_slashes",
    "num_digits",
    "num_special_chars",
    "has_at",
    "has_ip",
    "has_https",
    "subdomain_depth",
    "path_length",
    "heuristic_score",
]


def extract_features(url: str, analyzer: URLAnalyzer) -> list[float]:
    """Extract numeric features from a single URL string."""
    from urllib.parse import urlparse
    import re

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""

    heuristic = analyzer.analyze(url)

    ip_re = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")

    return [
        len(url),
        url.count("."),
        url.count("-"),
        url.count("/"),
        sum(c.isdigit() for c in url),
        sum(c in "@?=&%#+" for c in url),
        int("@" in url),
        int(bool(ip_re.match(hostname))),
        int(parsed.scheme == "https"),
        hostname.count("."),
        len(path),
        heuristic["score"],
    ]


def build_feature_matrix(urls: list[str], analyzer: URLAnalyzer) -> np.ndarray:
    rows = []
    for url in urls:
        try:
            rows.append(extract_features(url, analyzer))
        except Exception:
            rows.append([0.0] * len(URL_FEATURES))
    return np.array(rows, dtype=np.float32)


# ── Training ──────────────────────────────────────────────────────────────────


def train(dataset_path: str, output_path: str, test_size: float = 0.2) -> None:
    print(f"[PhishGuard] Loading dataset from {dataset_path}")
    df = pd.read_csv(dataset_path)

    if "url" not in df.columns or "label" not in df.columns:
        raise ValueError("Dataset must contain 'url' and 'label' columns.")

    urls = df["url"].tolist()
    labels = df["label"].tolist()

    analyzer = URLAnalyzer()
    print(f"[PhishGuard] Extracting features for {len(urls)} samples…")
    X = build_feature_matrix(urls, analyzer)
    y = np.array(labels, dtype=np.int32)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)),
        ]
    )

    print("[PhishGuard] Training Random Forest…")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    print("\n── Classification Report ──")
    print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"]))
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}\n")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump({"model": pipeline, "features": URL_FEATURES}, output_path)
    print(f"[PhishGuard] Model saved to {output_path}")


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train the PhishGuard AI model.")
    parser.add_argument(
        "--dataset",
        default="datasets/phishing_dataset.csv",
        help="Path to the labelled CSV dataset.",
    )
    parser.add_argument(
        "--output",
        default="models/phishguard_model.joblib",
        help="Path to save the trained model.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Fraction of data to use for evaluation (default: 0.2).",
    )
    args = parser.parse_args()
    train(args.dataset, args.output, args.test_size)
