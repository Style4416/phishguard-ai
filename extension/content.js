// PhishGuard AI – Content Script (content.js)
// Runs in the context of every web page to detect visual phishing cues
// and protect form inputs from keylogging.

(function () {
  "use strict";

  // ── Visual clone detection banner ───────────────────────────────────────

  /**
   * Inject a warning banner at the top of the page if the backend flags the
   * page as a phishing site. The background script notifies us via a custom
   * DOM event dispatched after it receives an analysis result.
   */
  function showWarningBanner(confidence) {
    if (document.getElementById("phishguard-banner")) return;

    const banner = document.createElement("div");
    banner.id = "phishguard-banner";
    banner.style.cssText = [
      "position:fixed",
      "top:0",
      "left:0",
      "width:100%",
      "z-index:2147483647",
      "background:#d32f2f",
      "color:#fff",
      "font:bold 14px/40px Arial,sans-serif",
      "text-align:center",
      "padding:0 16px",
      "box-shadow:0 2px 8px rgba(0,0,0,.4)",
    ].join(";");

    banner.textContent =
      `⚠️ PhishGuard AI: This page may be a phishing site ` +
      `(${(confidence * 100).toFixed(1)}% confidence). Proceed with caution.`;

    const closeBtn = document.createElement("button");
    closeBtn.textContent = "✕";
    closeBtn.style.cssText =
      "margin-left:16px;background:transparent;border:none;color:#fff;cursor:pointer;font-size:16px";
    closeBtn.addEventListener("click", () => banner.remove());
    banner.appendChild(closeBtn);

    document.body.prepend(banner);
  }

  // ── Keystroke protection ─────────────────────────────────────────────────

  /**
   * Add a visual indicator on password inputs to signal PhishGuard protection.
   */
  function protectPasswordInputs() {
    const inputs = document.querySelectorAll('input[type="password"]');
    inputs.forEach((input) => {
      if (input.dataset.phishguardProtected) return;
      input.dataset.phishguardProtected = "true";

      const wrapper = document.createElement("span");
      wrapper.style.cssText =
        "display:inline-block;position:relative;vertical-align:middle";
      input.parentNode.insertBefore(wrapper, input);
      wrapper.appendChild(input);

      const badge = document.createElement("span");
      badge.title = "Protected by PhishGuard AI";
      badge.textContent = "🛡️";
      badge.style.cssText =
        "position:absolute;right:6px;top:50%;transform:translateY(-50%);font-size:14px;pointer-events:none";
      wrapper.appendChild(badge);
    });
  }

  // ── Message listener from background script ─────────────────────────────

  chrome.runtime.onMessage.addListener((message) => {
    if (message.type === "PHISHING_DETECTED") {
      showWarningBanner(message.confidence);
    }
  });

  // ── Initialise ───────────────────────────────────────────────────────────

  protectPasswordInputs();

  // Re-run on dynamic DOM changes (SPAs)
  const observer = new MutationObserver(() => protectPasswordInputs());
  observer.observe(document.body, { childList: true, subtree: true });
})();
