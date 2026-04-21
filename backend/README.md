# PhishGuard AI – Backend

FastAPI-based REST API that analyses URLs for phishing indicators using heuristics, WHOIS data, SSL inspection, and an ML model.

## Quick Start

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # fill in your API keys
uvicorn main:app --reload
```

The API will be available at **http://localhost:8000**.  
Interactive docs: **http://localhost:8000/docs**

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/analyze` | Analyse a URL for phishing |

### POST /analyze

**Request body:**
```json
{ "url": "https://example.com" }
```

**Response:**
```json
{
  "url": "https://example.com",
  "is_phishing": false,
  "confidence": 0.12,
  "risk_factors": [],
  "details": { ... }
}
```

## Detectors

| Module | Description |
|--------|-------------|
| `url_analyzer.py` | Heuristic URL feature analysis |
| `whois_checker.py` | Domain age & WHOIS data inspection |
| `ssl_checker.py` | TLS certificate validity checks |
| `visual_detector.py` | Visual clone detection (CNN/perceptual hash) |

## Running Tests

```bash
pytest tests/ -v
```
