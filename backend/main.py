"""PhishGuard AI – FastAPI Backend Entry Point."""

from __future__ import annotations

import os
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

from detectors.url_analyzer import URLAnalyzer
from detectors.whois_checker import WHOISChecker
from detectors.ssl_checker import SSLChecker

# ── App setup ────────────────────────────────────────────────────────────────

app = FastAPI(
    title="PhishGuard AI API",
    description="Real-time phishing detection powered by ML and heuristic analysis.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Detector instances ────────────────────────────────────────────────────────

url_analyzer = URLAnalyzer()
whois_checker = WHOISChecker()
ssl_checker = SSLChecker()

# ── Schemas ───────────────────────────────────────────────────────────────────


class AnalyzeRequest(BaseModel):
    url: HttpUrl


class AnalyzeResponse(BaseModel):
    url: str
    is_phishing: bool
    confidence: float
    risk_factors: List[str]
    details: dict


# ── Routes ────────────────────────────────────────────────────────────────────


@app.get("/", tags=["Health"])
def health_check():
    """Returns service status."""
    return {"status": "ok", "service": "PhishGuard AI"}


@app.post("/analyze", response_model=AnalyzeResponse, tags=["Analysis"])
async def analyze_url(body: AnalyzeRequest):
    """
    Analyse a URL for phishing indicators.

    Returns a risk assessment with confidence score and enumerated risk factors.
    """
    url_str = str(body.url)

    try:
        url_result = url_analyzer.analyze(url_str)
        whois_result = whois_checker.check(url_str)
        ssl_result = ssl_checker.check(url_str)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    # Aggregate risk factors
    risk_factors: List[str] = (
        url_result.get("risk_factors", [])
        + whois_result.get("risk_factors", [])
        + ssl_result.get("risk_factors", [])
    )

    # Weighted confidence (simple average – replace with ML model score)
    scores = [
        url_result.get("score", 0.0),
        whois_result.get("score", 0.0),
        ssl_result.get("score", 0.0),
    ]
    confidence = round(sum(scores) / len(scores), 4)

    return AnalyzeResponse(
        url=url_str,
        is_phishing=confidence >= 0.5,
        confidence=confidence,
        risk_factors=risk_factors,
        details={
            "url_analysis": url_result,
            "whois": whois_result,
            "ssl": ssl_result,
        },
    )
