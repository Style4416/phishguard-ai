# phishguard-ai
🛡️ AI-powered real-time phishing detection browser extension with               explainable AI, visual clone detection, and keystroke protection.               Built for Rising India Hackthon 1.0 ] 2026.

<div align="center">

![PhishGuard AI Banner](assets/banner.png)

# 🛡️ PhishGuard AI

### Real-time AI-Powered Phishing Detection Browser Extension

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://www.javascript.com/)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-green.svg)](https://chrome.google.com/webstore)
[![Hackathon](https://img.shields.io/badge/Hackathon-2025-red.svg)](#)
[![Contributors](https://img.shields.io/github/contributors/YOUR_USERNAME/phishguard-ai)](https://github.com/YOUR_USERNAME/phishguard-ai/graphs/contributors)

**Protecting users from phishing attacks with explainable AI, visual clone detection, and real-time keystroke protection.**

[Demo Video](#) • [Report Bug](../../issues) • [Request Feature](../../issues)

</div>

---

## 📖 Table of Contents

- [About The Project](#-about-the-project)
- [Key Features](#-key-features)
- [What Makes Us Unique](#-what-makes-us-unique)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Demo](#-demo)
- [Team](#-team)
- [License](#-license)

---

## 🎯 About The Project

Phishing attacks cost the world **over $10 billion in 2023**, with 3.4 billion phishing emails sent daily. Traditional blacklist-based tools are **reactive** and miss zero-day phishing sites.

**PhishGuard AI** is a next-generation browser extension that uses **multi-layered AI detection** to protect users in real-time, with transparent explanations for every alert.

---

## ✨ Key Features

- 🚀 **Real-time Detection** — Analyzes URLs instantly as you browse
- 🧠 **Explainable AI** — Tells you *why* a site is flagged
- 🎨 **Visual Clone Detection** — CNN identifies sites mimicking PayPal, Google, etc.
- 🔊 **Voice Alerts** — Accessibility-first warnings
- 🛡️ **Keystroke Shield** — Blocks password entry on suspicious sites
- 📴 **Offline Mode** — TinyML model works without internet
- 📊 **Risk Score System** — 0-100 score instead of binary safe/unsafe
- 🌐 **Multi-layer Analysis** — URL, WHOIS, SSL, visual, behavioral

---

## 🌟 What Makes Us Unique

| Feature | PhishGuard AI | Traditional Tools |
|---------|:-------------:|:-----------------:|
| Zero-day detection | ✅ | ❌ |
| Explainable decisions | ✅ | ❌ |
| Visual AI clone detection | ✅ | ❌ |
| Voice accessibility | ✅ | ❌ |
| Keystroke protection | ✅ | ❌ |
| Offline capability | ✅ | ❌ |

---

## 🛠️ Tech Stack

**Frontend (Extension):**
- JavaScript (ES6+)
- Chrome Manifest V3
- HTML5 / CSS3

**Backend:**
- Python 3.10+
- FastAPI
- Uvicorn

**Machine Learning:**
- TensorFlow / Keras
- scikit-learn
- OpenCV (visual detection)

**APIs & Services:**
- Google Safe Browsing API
- WHOIS
- PhishTank
- VirusTotal

---

## 🏗️ Architecture

![Architecture Diagram](docs/images/architecture-diagram.png)

Our system uses a **4-layer detection pipeline**:
1. **Local Heuristics** (instant, <50ms)
2. **Reputation APIs** (100-500ms)
3. **ML Content Analysis** (on-demand)
4. **Risk Aggregation & XAI**

---

## 🚀 Getting Started

### Prerequisites
- Node.js v18+
- Python 3.10+
- Google Chrome / Edge
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/phishguard-ai.git
   cd phishguard-ai
