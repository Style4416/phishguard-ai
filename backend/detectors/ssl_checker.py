"""SSL Checker – validates TLS certificate details for phishing signals."""

from __future__ import annotations

import datetime
import socket
import ssl
from typing import Any, Dict
from urllib.parse import urlparse


class SSLChecker:
    """Check SSL/TLS certificate validity and age."""

    def check(self, url: str) -> Dict[str, Any]:
        """
        Inspect the TLS certificate of the given URL's host.

        Returns a dict with keys:
            score (float 0-1): phishing probability estimate
            risk_factors (list[str]): human-readable risk descriptions
        """
        risk_factors: list[str] = []
        score = 0.0

        parsed = urlparse(url)
        hostname = parsed.hostname or ""

        # No SSL at all
        if parsed.scheme != "https":
            risk_factors.append("Site does not use HTTPS – no SSL/TLS certificate")
            score += 0.2
            return {
                "score": min(round(score, 4), 1.0),
                "risk_factors": risk_factors,
                "has_ssl": False,
                "issuer": None,
                "expires_in_days": None,
            }

        cert_info: dict = {}
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(
                socket.create_connection((hostname, 443), timeout=5),
                server_hostname=hostname,
            ) as ssock:
                cert = ssock.getpeercert()
                cert_info = cert or {}
        except ssl.SSLCertVerificationError:
            risk_factors.append("SSL certificate verification failed (untrusted or self-signed)")
            score += 0.4
            return {
                "score": min(round(score, 4), 1.0),
                "risk_factors": risk_factors,
                "has_ssl": True,
                "issuer": None,
                "expires_in_days": None,
            }
        except Exception:
            risk_factors.append("Could not retrieve SSL certificate information")
            score += 0.1
            return {
                "score": min(round(score, 4), 1.0),
                "risk_factors": risk_factors,
                "has_ssl": True,
                "issuer": None,
                "expires_in_days": None,
            }

        # Parse expiry
        expires_in_days: int | None = None
        not_after = cert_info.get("notAfter")
        if not_after:
            expiry_dt = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            expires_in_days = (expiry_dt - datetime.datetime.utcnow()).days
            if expires_in_days < 0:
                risk_factors.append("SSL certificate has expired")
                score += 0.5
            elif expires_in_days < 10:
                risk_factors.append(
                    f"SSL certificate expires very soon ({expires_in_days} days)"
                )
                score += 0.2

        # Extract issuer
        issuer_raw = cert_info.get("issuer", ())
        issuer_dict = {k: v for pair in issuer_raw for k, v in pair}
        issuer = issuer_dict.get("organizationName") or issuer_dict.get("commonName")

        # DV-only cert from a free CA on a new site is a mild risk indicator
        if issuer and "let's encrypt" in issuer.lower():
            # Not conclusive, just mildly informational
            pass

        return {
            "score": min(round(score, 4), 1.0),
            "risk_factors": risk_factors,
            "has_ssl": True,
            "issuer": issuer,
            "expires_in_days": expires_in_days,
        }
