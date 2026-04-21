# Contributing to PhishGuard AI

Thank you for your interest in contributing to PhishGuard AI! 🛡️

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/<your-username>/phishguard-ai.git
   cd phishguard-ai
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and commit them (see [Coding Standards](#coding-standards))
5. **Push** your branch and open a **Pull Request**

## Development Setup

### Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

### Browser Extension
Load the `extension/` folder as an unpacked extension in Chrome/Edge:
1. Navigate to `chrome://extensions`
2. Enable **Developer Mode**
3. Click **Load unpacked** and select the `extension/` folder

### ML Model
```bash
cd ml-model
pip install -r ../backend/requirements.txt
python train.py
```

## Pull Request Process

1. Ensure your code follows the [Coding Standards](#coding-standards).
2. Update documentation and tests where applicable.
3. Add a clear description of the change and the motivation behind it.
4. Link to any related issues using `Closes #<issue-number>`.
5. A maintainer will review your PR within 5 business days.

## Coding Standards

- **Python**: Follow [PEP 8](https://peps.python.org/pep-0008/). Use type hints.
- **JavaScript**: Follow [Airbnb JS Style Guide](https://github.com/airbnb/javascript). Use `const`/`let`.
- **Commits**: Use [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, etc.)
- **Tests**: Every new feature or bug fix must include tests.

## Reporting Bugs

Open a [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) issue and include:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behaviour
- Environment details (OS, browser version, etc.)

## Suggesting Features

Open a [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) issue with:
- The problem your feature solves
- A proposed solution
- Any alternatives you considered
