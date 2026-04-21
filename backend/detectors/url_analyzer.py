"""URL Analyzer – heuristic-based phishing URL detector."""

from __future__ import annotations

import re
from urllib.parse import urlparse
from typing import Dict, Any


# Known legitimate TLDs that are often spoofed
SUSPICIOUS_TLDS = {".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".click"}

# Common brand names used in phishing URLs
BRAND_KEYWORDS = [
    "paypal", "apple", "amazon", "google", "microsoft", "facebook",
    "netflix", "instagram", "linkedin", "twitter", "bank", "secure",
    "account", "login", "signin", "verify", "update", "confirm",
]

# Regex for IP-based URLs
IP_URL_RE = re.compile(
    r"https?://(\d{1,3}\.){3}\d{1,3}"
)


class URLAnalyzer:
    """Analyse a URL for phishing heuristics."""

    def analyze(self, url: str) -> Dict[str, Any]:
        """
        Perform heuristic analysis on the given URL.

        Returns a dict with keys:
            score (float 0-1): phishing probability estimate
            risk_factors (list[str]): human-readable risk descriptions
        """
        risk_factors: list[str] = []
        score = 0.0

        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        path = parsed.path or ""
        full = url.lower()

        # Check for IP address instead of domain name
        if IP_URL_RE.match(url):
            risk_factors.append("URL uses an IP address instead of a domain name")
            score += 0.3

        # Excessive subdomains (> 3 dots in hostname)
        if hostname.count(".") > 3:
            risk_factors.append("Excessive number of subdomains detected")
            score += 0.15

        # Suspicious TLD
        for tld in SUSPICIOUS_TLDS:
            if hostname.endswith(tld):
                risk_factors.append(f"Uses a suspicious free TLD: {tld}")
                score += 0.2
                break

        # Brand keyword in subdomain / path (not in registered domain)
        parts = hostname.split(".")
        subdomain = ".".join(parts[:-2]) if len(parts) > 2 else ""
        for kw in BRAND_KEYWORDS:
            if kw in subdomain or kw in path.lower():
                risk_factors.append(
                    f"Brand keyword '{kw}' found in URL path or subdomain"
                )
                score += 0.2
                break

        # URL length > 75 chars
        if len(url) > 75:
            risk_factors.append("URL is unusually long (> 75 characters)")
            score += 0.1

        # Contains '@' symbol (often used to deceive)
        if "@" in url:
            risk_factors.append("URL contains '@' symbol which can mask the real destination")
            score += 0.25

        # Double slash in path
        if "//" in path:
            risk_factors.append("URL path contains double slashes")
            score += 0.1

        # Hyphen in domain (common in phishing)
        if "-" in hostname:
            risk_factors.append("Domain name contains hyphens (common in phishing domains)")
            score += 0.1

        # HTTP (not HTTPS)
        if parsed.scheme == "http":
            risk_factors.append("Connection is not encrypted (HTTP instead of HTTPS)")
            score += 0.15

        return {
            "score": min(round(score, 4), 1.0),
            "risk_factors": risk_factors,
            "hostname": hostname,
            "scheme": parsed.scheme,
        }
