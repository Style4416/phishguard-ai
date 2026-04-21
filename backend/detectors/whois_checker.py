"""WHOIS Checker – checks domain registration details for phishing signals."""

from __future__ import annotations

import datetime
from typing import Any, Dict
from urllib.parse import urlparse


class WHOISChecker:
    """Perform WHOIS-based analysis on a URL's domain."""

    def check(self, url: str) -> Dict[str, Any]:
        """
        Check WHOIS information for phishing indicators.

        Returns a dict with keys:
            score (float 0-1): phishing probability estimate
            risk_factors (list[str]): human-readable risk descriptions
        """
        risk_factors: list[str] = []
        score = 0.0
        domain_age_days: int | None = None
        registrar: str | None = None

        hostname = urlparse(url).hostname or ""

        try:
            import whois  # type: ignore

            w = whois.whois(hostname)

            # Domain age check
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            if creation_date:
                if isinstance(creation_date, str):
                    creation_date = datetime.datetime.fromisoformat(creation_date)
                age = (datetime.datetime.utcnow() - creation_date).days
                domain_age_days = age
                if age < 30:
                    risk_factors.append(
                        f"Domain is very new (registered {age} days ago)"
                    )
                    score += 0.35
                elif age < 180:
                    risk_factors.append(
                        f"Domain is relatively new (registered {age} days ago)"
                    )
                    score += 0.15

            registrar = w.registrar

        except Exception:
            # WHOIS lookup failed – treat as mildly suspicious
            risk_factors.append("WHOIS information could not be retrieved for this domain")
            score += 0.1

        return {
            "score": min(round(score, 4), 1.0),
            "risk_factors": risk_factors,
            "domain": hostname,
            "domain_age_days": domain_age_days,
            "registrar": registrar,
        }
