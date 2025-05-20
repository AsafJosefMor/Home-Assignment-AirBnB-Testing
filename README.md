---

# Automation Framework (Pytest + Playwright) for a home assignment

## Overview
A browser automation framework using `pytest-playwright` only. Built with modularity, configurability, and test clarity in mind for a home assignment.

---

## Features
- End-to-end test: Airbnb search + reservation
- Page Object Model (POM)
- Config via `.env` + `config.py`
- Plugin: `--suite-timeout` using environment variable
- Screenshots and HTML test reports
- Docker + Makefile support

---

## Project Structure

```
.
 config/                # Configuration, test data, and selectors
 pages/                 # Page Object Models
 tests/                 # Test cases (pytest)
 utils/                 # Plugins and logging utilities
 tests/reports/         # HTML reports, screenshots, JSON results
 run.sh                 # One-liner to setup and run locally
 Dockerfile             # Test runner container
 docker-compose.yml     # Docker execution
 requirements.txt
 Makefile
 pytest.ini
 README.md
```

---

## Manual Run with .env

```bash
export $(grep -v '^#' .env | xargs -d '\n')
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install .
playwright install
pytest --suite-timeout=$SUITE_TIMEOUT_SEC # Defaults to 15 minutes suite timeout
```

Or just:

```bash
bash run.sh
```

---

## Environment Variables

| Variable               | Default      | Description                              |
|------------------------|--------------|------------------------------------------|
| `BASE_URL`             | airbnb.com   | URL for the test subject                 |
| `WAIT_AFTER_ACTION_MS` | 5000         | Delay (in ms) between UI interactions    |
| `SUITE_TIMEOUT_SEC`    | 900 (15 min) | Timeout for full test suite (in seconds) |

---

## Adding New Tests

1. Create a new file in `tests/`.
2. Use the `page` fixture from `pytest-playwright`.
3. Import POMs from `pages/`, config values/selectors from `config/`.

---

## Test Outputs

- HTML Report  `tests/reports/report.html`
- Screenshots  `tests/reports/<test>_failure.png`
- Best result  `tests/reports/result.json`
- Reservation details  `tests/reports/reservation.json`

---

## Docker Support

```bash
docker-compose up --build
```

Builds the test runner and executes the suite with environment-configurable headless mode.

---

If you encounter this error:

> The virtual environment was not created successfully because ensurepip is not available...

Run this once to fix it:

```bash
sudo apt install python3-venv
```

Then rerun setup using `run.sh` or manually.

---

## Test Data (config/test_data.json)

All tests are driven by values defined in `config/test_data.json`, which includes:

```json
{
  "location": "Tel Aviv",
  "adults": 2,
  "children": 1,
  "checkin": "2025-06-18",
  "checkout": "2025-06-20",
  "phone": "505555555"
}
```

To add more test cases:
- Create additional JSON blocks
- Use `@pytest.mark.parametrize` to load and run multiple inputs

---

## Out of Scope

This project was developed under short assignment constraints, and deliberately excludes the following:

- In-depth logging
- Code style and linting
- Date Picker Pagination: The test uses only dates from the first visible month in the Airbnb calendar (next month). No pagination logic was implemented to navigate calendar months.
- Listings Pagination Limit: All listings across all pages are evaluated. No environment variable was implemented to limit pages scanned.
- Code Review and Commit Hygiene: This is a one-person home assignment and was not built with Git collaboration or commit structuring.
- Language Support: The test assumes the Airbnb UI is displayed in English. Changing site language may cause DOM inconsistencies or selector failures.
- Test Flakiness Handling: Airbnb uses rich animations and dynamic DOM updates. The test does not currently support retries or advanced recovery on failures.
- Minimal Use of Waits: Basic waits were added only where strictly necessary to complete flows without flakiness. No full stabilization logic.
- User Mode Support: All flows were developed and tested in Guest (unauthenticated) mode. No login flow or user-specific flows were included.
- Browser Support: Written and tested against Chromium only. Other browsers (Firefox, WebKit) are not guaranteed to work.
- Pricing Accuracy: Price comparisons use the per-night price only. They do not include cleaning fees, taxes, or total booking cost.
- Test Coverage: Testing was limited due to tight deadlines and was not comprehensive or systematic.

---
