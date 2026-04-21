// PhishGuard AI – Service Worker (background.js)
// Intercepts navigation events and checks URLs against the backend API.

const API_BASE_URL = "http://localhost:8000";

// ── Helpers ──────────────────────────────────────────────────────────────────

/**
 * Send a URL to the PhishGuard backend for analysis.
 * @param {string} url
 * @returns {Promise<{is_phishing: boolean, confidence: number, risk_factors: string[]}>}
 */
async function analyzeUrl(url) {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  if (!response.ok) {
    throw new Error(`Backend returned ${response.status}`);
  }
  return response.json();
}

/**
 * Store analysis result for a given tab so the popup can read it.
 * @param {number} tabId
 * @param {object} result
 */
function cacheResult(tabId, result) {
  chrome.storage.session.set({ [`result_${tabId}`]: result });
}

// ── Navigation listener ───────────────────────────────────────────────────────

chrome.webNavigation.onCommitted.addListener(
  async (details) => {
    if (details.frameId !== 0) return; // main frame only
    const { tabId, url } = details;

    if (!url.startsWith("http://") && !url.startsWith("https://")) return;

    try {
      const result = await analyzeUrl(url);
      cacheResult(tabId, { url, ...result, timestamp: Date.now() });

      if (result.is_phishing && result.confidence >= 0.8) {
        chrome.notifications.create(`phish_${tabId}`, {
          type: "basic",
          iconUrl: "icons/icon48.png",
          title: "⚠️ PhishGuard AI Warning",
          message: `Potential phishing page detected!\nConfidence: ${(result.confidence * 100).toFixed(1)}%`,
          priority: 2,
        });
      }
    } catch (err) {
      console.error("[PhishGuard] Analysis failed:", err);
      cacheResult(tabId, { url, error: err.message, timestamp: Date.now() });
    }
  },
  { url: [{ schemes: ["http", "https"] }] }
);

// ── Message listener (popup ↔ background) ────────────────────────────────────

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "GET_RESULT") {
    chrome.storage.session.get(`result_${message.tabId}`, (data) => {
      sendResponse(data[`result_${message.tabId}`] || null);
    });
    return true; // keep message channel open for async response
  }
});
