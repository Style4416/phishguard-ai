# PhishGuard AI – Machine Learning Model

This directory contains training and inference code for the PhishGuard AI phishing classification model.

## Directory Structure

```
ml-model/
├── train.py          # Training script (Random Forest + feature pipeline)
├── predict.py        # Inference module (CLI + importable API)
├── datasets/         # Place labelled CSV datasets here
├── models/           # Trained model artefacts (.joblib)
└── notebooks/        # Jupyter notebooks for EDA & experiments
```

## Dataset Format

Place a CSV file in `datasets/` with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `url`  | str  | Raw URL string |
| `label`| int  | `1` = phishing, `0` = legitimate |

Recommended public datasets:
- [PhiUSIIL Phishing URL Dataset (UCI)](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset)
- [PhishTank](https://phishtank.org/developer_info.php)

## Training

```bash
cd ml-model
python train.py \
  --dataset datasets/phishing_dataset.csv \
  --output  models/phishguard_model.joblib \
  --test-size 0.2
```

## Prediction

```bash
# CLI
python predict.py --url "https://paypal-verify.tk/login"

# Python API
from predict import predict
result = predict("https://paypal-verify.tk/login")
print(result)
```

## Features Used

| Feature | Description |
|---------|-------------|
| `url_length` | Total character length of URL |
| `num_dots` | Number of dots |
| `num_hyphens` | Number of hyphens |
| `num_slashes` | Number of slashes |
| `num_digits` | Digit count |
| `num_special_chars` | Count of `@?=&%#+` |
| `has_at` | Contains `@` symbol |
| `has_ip` | Hostname is an IP address |
| `has_https` | Uses HTTPS scheme |
| `subdomain_depth` | Number of dots in hostname |
| `path_length` | Length of URL path |
| `heuristic_score` | Score from `URLAnalyzer` heuristics |
