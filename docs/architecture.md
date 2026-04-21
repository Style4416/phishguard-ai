# PhishGuard AI – Architecture

## Overview

PhishGuard AI is composed of three main components that communicate in a request–response pipeline:

```
Browser                      Backend (FastAPI)              ML / Data
──────────────               ─────────────────              ──────────
Extension popup  ──POST──►  /analyze endpoint  ──────────► URLAnalyzer
Content script               │                              WHOISChecker
Background SW                │                              SSLChecker
                             │                              VisualDetector
                             │                              │
                             └────────────────────────────► RandomForest model
                                      ◄── JSON response ──
```

## Component Details

### 1. Browser Extension (Manifest V3)

| File | Responsibility |
|------|----------------|
| `background.js` (service worker) | Intercepts navigation events; calls `/analyze`; caches results per tab |
| `content.js` | Injects phishing warning banner; adds keystroke-protection badge on password fields |
| `popup.html/js/css` | Displays risk verdict, confidence bar, and risk factor list for the active tab |

### 2. FastAPI Backend

Stateless REST API. Each request is independent.

```
POST /analyze
  ├── URLAnalyzer.analyze()        → heuristic URL score
  ├── WHOISChecker.check()         → domain age / registrar
  ├── SSLChecker.check()           → TLS cert validity
  └── (future) VisualDetector.compare() → screenshot similarity
```

Risk scores from each detector are averaged into a single `confidence` value (0–1).  
`is_phishing = confidence ≥ 0.5`

### 3. ML Model Pipeline

```
Raw URL
  └─► Feature extraction (12 numeric features)
        └─► StandardScaler
              └─► RandomForestClassifier (200 trees)
                    └─► P(phishing)
```

The trained model is persisted as `ml-model/models/phishguard_model.joblib`.  
When no model file is found the backend falls back to heuristic scores only.

## Data Flow Diagram

```
User visits URL
     │
     ▼
background.js intercepts navigation
     │
     ▼  POST /analyze {"url": "..."}
FastAPI backend
     ├── URLAnalyzer   → score, risk_factors
     ├── WHOISChecker  → score, domain_age
     └── SSLChecker    → score, cert_info
     │
     ▼  JSON response
background.js caches result for tab
     │
     ├──► If confidence ≥ 0.8 → Chrome notification
     └──► Popup reads cached result on click
```

## Security Considerations

- The backend never stores or logs analysed URLs beyond the current request.
- All inter-component communication uses HTTPS in production.
- The extension uses Manifest V3 (service worker, restricted host permissions).
- CORS is restricted to the extension origin in production.
