# PhishGuard AI – Setup Guide

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | ≥ 3.11 | Backend & ML model |
| pip | ≥ 23 | Python package manager |
| Chrome / Edge | Latest | Browser extension |
| Git | ≥ 2.40 | Clone the repository |

---

## 1. Clone the Repository

```bash
git clone https://github.com/Style4416/phishguard-ai.git
cd phishguard-ai
```

---

## 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and fill in any optional API keys (e.g. VirusTotal).

**Start the server:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Verify it's running:
```bash
curl http://localhost:8000/
# {"status":"ok","service":"PhishGuard AI"}
```

---

## 3. Browser Extension Setup

1. Open **Chrome** or **Edge** and navigate to `chrome://extensions`.
2. Enable **Developer Mode** (toggle in the top-right corner).
3. Click **Load unpacked** and select the `extension/` folder.
4. The PhishGuard AI shield icon will appear in the toolbar.

> **Note:** The extension expects the backend at `http://localhost:8000`.  
> To change this, update `API_BASE_URL` in `extension/background.js`.

---

## 4. ML Model Training (Optional)

If you have a labelled phishing dataset:

```bash
cd ml-model
python train.py \
  --dataset datasets/phishing_dataset.csv \
  --output  models/phishguard_model.joblib
```

The backend will automatically load the model on startup if the file exists at the path specified in `.env` (`MODEL_PATH`).

---

## 5. Running Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

---

## 6. Environment Variables Reference

See [`backend/.env.example`](../backend/.env.example) for the full list of configurable variables.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'fastapi'` | Activate your virtual environment and run `pip install -r requirements.txt` |
| Extension shows "No analysis available" | Ensure the backend is running and reload the page |
| CORS error in browser console | Add the extension origin to `ALLOWED_ORIGINS` in `.env` |
| WHOIS lookup times out | This is expected for some domains; the backend will flag it as a minor risk and continue |
