"""Visual Detector – detects visual clones of known legitimate websites."""

from __future__ import annotations

from typing import Any, Dict


class VisualDetector:
    """
    Compare the visual layout of a page screenshot against a reference database
    of known legitimate sites to detect clone phishing pages.

    This is a placeholder implementation. In production, replace `compare`
    with a trained CNN/perceptual-hash model loaded from `ml-model/models/`.
    """

    def compare(self, screenshot_bytes: bytes, reference_brand: str) -> Dict[str, Any]:
        """
        Compare a page screenshot against the reference for *reference_brand*.

        Parameters
        ----------
        screenshot_bytes:
            Raw PNG/JPEG bytes of the target page screenshot.
        reference_brand:
            The brand name to compare against (e.g. ``"paypal"``, ``"google"``).

        Returns
        -------
        dict with keys:
            is_clone (bool): True if the page looks like a clone.
            similarity (float): 0–1 visual similarity score.
            risk_factors (list[str]): Human-readable risk descriptions.
        """
        # TODO: Load a trained perceptual-hash / CNN model and compute real
        # similarity. The stub below always returns a "safe" result.
        return {
            "is_clone": False,
            "similarity": 0.0,
            "risk_factors": [],
        }
