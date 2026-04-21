# PhishGuard AI – Browser Extension

This directory contains the **Manifest V3** Chrome/Edge browser extension that provides real-time phishing protection.

## File Structure

```
extension/
├── manifest.json      # Extension manifest (MV3)
├── background.js      # Service worker – URL interception & analysis
├── content.js         # Content script – visual banner & keystroke protection
├── popup.html         # Extension popup UI
├── popup.js           # Popup logic
├── styles/
│   └── popup.css      # Popup stylesheet
└── icons/             # Extension icons (16×16, 48×48, 128×128 PNG)
```

## Development Setup

1. Open **Chrome** (or Edge) and navigate to `chrome://extensions`.
2. Enable **Developer Mode** (toggle in the top-right corner).
3. Click **Load unpacked** and select this `extension/` directory.
4. The PhishGuard AI icon will appear in the toolbar.

## Configuration

By default the extension communicates with the backend at `http://localhost:8000`.  
To change this, update the `API_BASE_URL` constant in `background.js`.

## Permissions Explained

| Permission | Reason |
|---|---|
| `activeTab` | Read the URL of the current tab |
| `storage` | Cache analysis results per tab |
| `webRequest` | Intercept navigation events |
| `notifications` | Show phishing alerts |
| `<all_urls>` | Analyse any visited URL |

## Adding Icons

Place PNG icons in the `icons/` directory:

```
icons/icon16.png    (16×16)
icons/icon48.png    (48×48)
icons/icon128.png   (128×128)
```
