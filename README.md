# Test Automation Suite

End-to-end test framework for a store web app and REST API. Built with Playwright, pytest, and k6.

## What's tested

| Layer | Tool | Tests |
|---|---|---|
| E2E browser (Chromium + Firefox) | Playwright + pytest | 54 tests |
| API load | k6 | 500 concurrent users |

## Stack

- Python 3.12, Playwright, pytest, pytest-xdist
- FastAPI (local target for k6)
- k6 for load testing
- GitHub Actions CI with Allure reports

## Run locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium firefox

# E2E tests (parallel across browsers)
pytest tests/ -n auto --browser chromium --browser firefox

# Load test (two terminals)
uvicorn app.main:app --port 8000
k6 run k6/load_test.js --env APP_BASE_URL=http://localhost:8000
```

## Results

- 108 E2E tests (54 per browser), parallel execution across Chromium + Firefox
- Sequential: 26 min 38 sec → Parallel: 4 min 48 sec (75% faster)
- k6: 500 VUs, 0% error rate, P95 login 268ms, P95 checkout 457ms

## Screenshots

See the [docs/](docs/) folder for Allure reports, pytest output, and k6 load test results.
