// PhishGuard AI – Popup Script (popup.js)

const $ = (id) => document.getElementById(id);

function showState(id) {
  ["state-loading", "state-safe", "state-phishing", "state-error"].forEach((s) => {
    $(s).classList.toggle("hidden", s !== id);
  });
}

function truncate(str, max = 60) {
  return str.length > max ? str.slice(0, max) + "…" : str;
}

async function init() {
  showState("state-loading");

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab) {
    showState("state-error");
    $("error-msg").textContent = "Could not determine active tab.";
    return;
  }

  chrome.runtime.sendMessage({ type: "GET_RESULT", tabId: tab.id }, (result) => {
    if (!result) {
      showState("state-error");
      $("error-msg").textContent = "No analysis available for this page yet.";
      return;
    }

    if (result.error) {
      showState("state-error");
      $("error-msg").textContent = result.error;
      return;
    }

    const pct = Math.round((result.confidence || 0) * 100);

    if (result.is_phishing) {
      showState("state-phishing");
      $("phish-url").textContent = truncate(result.url || "");
      $("phish-bar").style.width = `${pct}%`;
      $("phish-pct").textContent = `${pct}%`;

      const list = $("risk-factors");
      list.innerHTML = "";
      (result.risk_factors || []).forEach((factor) => {
        const li = document.createElement("li");
        li.textContent = factor;
        list.appendChild(li);
      });
    } else {
      showState("state-safe");
      $("safe-url").textContent = truncate(result.url || "");
      const safeConfidence = Math.round((1 - (result.confidence || 0)) * 100);
      $("safe-bar").style.width = `${safeConfidence}%`;
      $("safe-pct").textContent = `${safeConfidence}%`;
    }
  });
}

document.addEventListener("DOMContentLoaded", init);
