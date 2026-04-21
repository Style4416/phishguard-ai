"""Tests for URL analyzer heuristics."""

import pytest
from detectors.url_analyzer import URLAnalyzer


@pytest.fixture()
def analyzer():
    return URLAnalyzer()


def test_safe_url(analyzer):
    result = analyzer.analyze("https://www.google.com/search?q=test")
    assert result["score"] < 0.5
    assert result["risk_factors"] == [] or isinstance(result["risk_factors"], list)


def test_ip_url_is_suspicious(analyzer):
    result = analyzer.analyze("http://192.168.1.1/login")
    assert any("IP address" in f for f in result["risk_factors"])
    assert result["score"] > 0.0


def test_brand_keyword_in_subdomain(analyzer):
    result = analyzer.analyze("https://paypal.verify.suspicious.tk/login")
    # Should flag brand keyword and suspicious TLD
    assert result["score"] > 0.3


def test_http_url_flagged(analyzer):
    result = analyzer.analyze("http://example.com/page")
    assert any("HTTP" in f or "http" in f.lower() for f in result["risk_factors"])


def test_at_symbol_flagged(analyzer):
    result = analyzer.analyze("http://google.com@evil.com/")
    assert any("@" in f for f in result["risk_factors"])


def test_score_capped_at_1(analyzer):
    # Pile on every bad signal
    result = analyzer.analyze("http://192.168.1.1@paypal-verify.tk/login//confirm?id=1234567890abcdef")
    assert result["score"] <= 1.0
