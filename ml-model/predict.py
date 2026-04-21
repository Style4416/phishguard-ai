"""
PhishGuard AI – Prediction Module
===================================
Loads a trained model and returns a phishing probability for a given URL.

Usage
-----
    python predict.py --url "https://suspicious-login.tk/paypal/verify"
    python predict.py --url "https://www.google.com"
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any, Dict

import joblib
import numpy as np

# Ensure backend detectors are importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
from detectors.url_analyzer import URLAnalyzer  # noqa: E402

DEFAULT_MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "models", "phishguard_model.joblib"
)

# Module-level cache so the model is only loaded once per process
_model_cache: Dict[str, Any] = {}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_model(model_path: str) -> Any:
    if model_path not in _model_cache:
        data = joblib.load(model_path)
        _model_cache[model_path] = data
    return _model_cache[model_path]


def _extract_features(url: str, analyzer: URLAnalyzer) -> np.ndarray:
    """Reuse the same feature extraction logic as train.py."""
    from urllib.parse import urlparse
    import re

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    heuristic = analyzer.analyze(url)
    ip_re = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")

    features = [
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
    return np.array([features], dtype=np.float32)


# ── Public API ────────────────────────────────────────────────────────────────

def predict(url: str, model_path: str = DEFAULT_MODEL_PATH) -> Dict[str, Any]:
    """
    Predict whether a URL is a phishing site.

    Parameters
    ----------
    url:
        The URL to analyse.
    model_path:
        Path to the trained ``.joblib`` model file.

    Returns
    -------
    dict with keys:
        url (str)
        is_phishing (bool)
        confidence (float): probability that the URL is phishing (0–1)
        heuristic_risk_factors (list[str])
    """
    analyzer = URLAnalyzer()
    heuristic = analyzer.analyze(url)

    if not os.path.exists(model_path):
        # Fall back to heuristics-only when no model is available
        confidence = heuristic["score"]
        return {
            "url": url,
            "is_phishing": confidence >= 0.5,
            "confidence": confidence,
            "heuristic_risk_factors": heuristic["risk_factors"],
            "model_used": False,
        }

    data = _load_model(model_path)
    pipeline = data["model"]
    X = _extract_features(url, analyzer)
    confidence = float(pipeline.predict_proba(X)[0, 1])

    return {
        "url": url,
        "is_phishing": confidence >= 0.5,
        "confidence": round(confidence, 4),
        "heuristic_risk_factors": heuristic["risk_factors"],
        "model_used": True,
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict phishing probability for a URL.")
    parser.add_argument("--url", required=True, help="URL to analyse.")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL_PATH,
        help="Path to the trained model file.",
    )
    args = parser.parse_args()

    result = predict(args.url, args.model)

    verdict = "⚠️  PHISHING" if result["is_phishing"] else "✅  SAFE"
    print(f"\n{verdict}")
    print(f"URL        : {result['url']}")
    print(f"Confidence : {result['confidence'] * 100:.1f}%")
    if result["heuristic_risk_factors"]:
        print("Risk factors:")
        for f in result["heuristic_risk_factors"]:
            print(f"  • {f}")
