# PhishGuard AI – API Documentation

## Base URL

```
http://localhost:8000        (development)
https://api.phishguard.ai   (production – placeholder)
```

## Authentication

No authentication is required in the current version.  
Production deployments should add API-key or JWT auth via a middleware.

---

## Endpoints

### GET /

Health check.

**Response 200**
```json
{
  "status": "ok",
  "service": "PhishGuard AI"
}
```

---

### POST /analyze

Analyse a URL for phishing indicators.

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string (URL) | ✅ | The fully-qualified URL to analyse |

```json
{
  "url": "https://paypal-verify.tk/login/confirm"
}
```

**Response 200** (`application/json`)

| Field | Type | Description |
|-------|------|-------------|
| `url` | string | The analysed URL |
| `is_phishing` | boolean | True if `confidence ≥ 0.5` |
| `confidence` | float (0–1) | Aggregate phishing probability |
| `risk_factors` | string[] | Human-readable risk descriptions |
| `details` | object | Per-detector raw results |

```json
{
  "url": "https://paypal-verify.tk/login/confirm",
  "is_phishing": true,
  "confidence": 0.6833,
  "risk_factors": [
    "Uses a suspicious free TLD: .tk",
    "Brand keyword 'paypal' found in URL path or subdomain",
    "Domain is very new (registered 12 days ago)"
  ],
  "details": {
    "url_analysis": {
      "score": 0.4,
      "risk_factors": [...],
      "hostname": "paypal-verify.tk",
      "scheme": "https"
    },
    "whois": {
      "score": 0.35,
      "risk_factors": [...],
      "domain": "paypal-verify.tk",
      "domain_age_days": 12,
      "registrar": "Freenom"
    },
    "ssl": {
      "score": 0.0,
      "risk_factors": [],
      "has_ssl": true,
      "issuer": "Let's Encrypt",
      "expires_in_days": 87
    }
  }
}
```

**Response 422** – Validation error (malformed URL)

```json
{
  "detail": [
    {
      "loc": ["body", "url"],
      "msg": "value is not a valid URL",
      "type": "value_error.url"
    }
  ]
}
```

**Response 500** – Internal analysis error

```json
{
  "detail": "Error description"
}
```

---

## Interactive Docs

When the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
