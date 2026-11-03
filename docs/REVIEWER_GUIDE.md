# Reviewer's Quick Start & Evaluation Guide

Welcome to the Restful Booker Platform Test Automation Framework hiring assessment repository. This guide gives a quick, 2-minute overview to help you navigate the codebase, understand architectural choices, and run the tests locally.

---

## 1. Quick Setup & Run (Under 2 Minutes)

### Prerequisites
- Python 3.11+
- Git

### Commands to Run

```bash
# 1. Clone the repository
git clone https://github.com/sameertatework1-lgtm/Interview_project.git
cd Interview_project

# 2. (Optional) Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 3. Install pinned dependencies & Chromium browser
pip install -r requirements.txt
playwright install chromium

# 4. Create local environment file from example
cp .env.example .env
# (The default values in .env.example point to the live public platform)

# 5. Run the high-priority Smoke Suite
pytest -m smoke -v

# 6. Run all API tests
pytest -m api -v

# 7. Run all UI tests (headed mode to watch the browser)
pytest -m ui --headed
```

---

## 2. Top 10 Files to Review First

To quickly assess the design quality, SDET maturity, and maintainability of this framework, we recommend opening these 10 files in order:

1. **`PLAN.md`**: Upfront SDET planning, architecture diagram, risk matrix for the public demo.
2. **`docs/DISCOVERY.md`**: Live system discovery notes resolving starred status codes, schema quirks, and reverse-proxy redirect bugs.
3. **`config/settings.py`**: Clean, env-driven configuration with validation and zero hardcoded URLs.
4. **`src/api/base_client.py`**: Robust REST client wrapping Playwright `APIRequestContext` with automatic Allure attachments on failure.
5. **`src/pages/base_page.py`**: Resilient base Page Object using Playwright auto-waiting, web-first assertions, and zero `time.sleep()` calls.
6. **`src/data/factories.py`**: Unique data generation (`AUTO_<epoch><rand>`) guaranteeing zero test crosstalk on the shared demo server.
7. **`tests/conftest.py`**: Multi-tier health check, session-cached auth, failure trace/screenshot capture, and reliable teardown cleanup fixtures.
8. **`features/api/rooms.feature` & `features/ui/admin_auth.feature`**: Clear, stakeholder-readable Gherkin scenarios with parameterization.
9. **`.github/workflows/tests.yml`**: Production-ready GitHub Actions CI/CD pipeline with artifact uploads and retries.
10. **`docs/TRACEABILITY.md`**: Complete traceability matrix linking all 83 manual test cases to automated scenarios.

---

## 3. Key Design Decisions

- **Why Playwright Sync?** Synchronous API avoids `async/await` fixture contention in pytest-bdd while natively handling browser automation and high-speed API requests in a unified context.
- **Why Zero Sleeps?** The entire codebase has 0 `time.sleep()` calls. We rely on Playwright's auto-waiting locators and web-first assertions (`expect(locator).to_be_visible()`).
- **Defect Transparency:** Known live server defects (such as `/actuator/health` returning 500) are explicitly marked with `@pytest.mark.xfail(reason=...)` rather than hidden.

