# 🛡️ PhishGuard AI

> **AI-powered real-time phishing detection** browser extension with explainable AI, visual clone detection, and keystroke protection.  
> Built for **Rising India Hackathon 1.0 – 2026**.

[![CI](https://github.com/Style4416/phishguard-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/Style4416/phishguard-ai/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Real-time URL Analysis** | Heuristic + ML-based phishing detection on every page visit |
| 🧠 **Explainable AI** | Human-readable risk factors surfaced in the popup |
| 👁️ **Visual Clone Detection** | Perceptual-hash comparison against reference screenshots |
| 🔐 **Keystroke Protection** | Password input fields visually guarded against credential harvesting |
| 📜 **WHOIS Inspection** | Domain age and registrar anomaly detection |
| 🔒 **SSL Validation** | TLS certificate expiry and trust-chain checks |

---

## 🗂️ Project Structure

```
phishguard-ai/
├── extension/          # Browser Extension (Manifest V3 – Chrome/Edge)
├── backend/            # FastAPI REST API
├── ml-model/           # Random Forest training & inference pipeline
├── docs/               # Architecture, API docs, setup guide
└── assets/             # Logos, banners, screenshots
```

---

## 🚀 Quick Start

### 1 · Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

### 2 · Browser Extension

1. Open `chrome://extensions` → enable **Developer Mode**
2. Click **Load unpacked** → select the `extension/` folder

Full instructions: [docs/setup-guide.md](docs/setup-guide.md)

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [Setup Guide](docs/setup-guide.md) | Installation and configuration |
| [Architecture](docs/architecture.md) | System design and data flow |
| [API Docs](docs/api-docs.md) | Backend REST API reference |
| [Contributing](CONTRIBUTING.md) | How to contribute |
| [Changelog](CHANGELOG.md) | Version history |

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md) first.

---

## 📄 License

[MIT](LICENSE) © 2026 Shoaib Amin Sayyed
