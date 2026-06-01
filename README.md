# PyTest API Automation Framework

A Python-based REST API validation framework built with PyTest, covering 90+ endpoints with automated quality gates integrated into GitLab CI/CD.

## Features

- Modular API client with session management and retry logic
- Schema validation on all responses
- Environment-based configuration (dev / staging / prod)
- Detailed HTML test reports via `pytest-html`
- Integrated into GitLab CI/CD — runs on every commit
- Parallel test execution with `pytest-xdist`

## Project Structure

```
pytest-api-automation-framework/
├── config/
│   └── config.yaml          # Environment configs
├── tests/
│   ├── test_health.py        # Health/readiness endpoint tests
│   ├── test_auth.py          # Auth & token validation tests
│   └── test_users.py         # User CRUD endpoint tests
├── utils/
│   ├── api_client.py         # Base HTTP client with retry/session
│   └── validators.py         # Response schema & status validators
├── conftest.py               # Shared fixtures
├── requirements.txt
└── .gitlab-ci.yml            # CI/CD pipeline config
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Tests

```bash
# All tests
pytest tests/ -v

# With HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html

# Parallel execution
pytest tests/ -v -n auto

# Specific suite
pytest tests/test_users.py -v
```

## Configuration

Edit `config/config.yaml` to set base URLs and credentials per environment:

```yaml
environments:
  dev:
    base_url: "https://api.dev.example.com"
  staging:
    base_url: "https://api.staging.example.com"
```

Set the active environment via env var:

```bash
export ENV=staging
pytest tests/ -v
```

## CI/CD Integration

The `.gitlab-ci.yml` runs the full test suite on every push and merge request, publishing the HTML report as a GitLab artifact.

## Tech Stack

- Python 3.10+
- PyTest
- Requests
- PyYAML
- pytest-html
- pytest-xdist
