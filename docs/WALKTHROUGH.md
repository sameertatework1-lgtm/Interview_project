# SDET Interview Walkthrough & Architecture Defense

> A plain-language guide explaining architectural choices, design rationale, flakiness handling, and future improvements.

---

## 1. Top 10 Files for Reviewers to Inspect First

If you have 5 minutes to inspect this framework, open these 10 files in order:

1. [`docs/DISCOVERY.md`](file:///e:/Interview_Project/docs/DISCOVERY.md) — The live system reverse-engineering report proving real API behaviors vs sheet assumptions.
2. [`docs/DECISIONS.md`](file:///e:/Interview_Project/docs/DECISIONS.md) — Architectural decision log (D-001 through D-009) explaining every design trade-off.
3. [`docs/TRACEABILITY.md`](file:///e:/Interview_Project/docs/TRACEABILITY.md) — 1:1 mapping from all 83 manual test cases to automated scenarios.
4. [`src/api/base_client.py`](file:///e:/Interview_Project/src/api/base_client.py) — Core API abstraction over Playwright `APIRequestContext` with automatic failure payload attachments to Allure.
5. [`src/pages/base_page.py`](file:///e:/Interview_Project/src/pages/base_page.py) — Foundation Page Object with zero-sleep auto-waiting and fallback mechanisms.
6. [`src/data/factories.py`](file:///e:/Interview_Project/src/data/factories.py) — Unique data generation ensuring collision-free runs on a shared public demo.
7. [`tests/conftest.py`](file:///e:/Interview_Project/tests/conftest.py) — Central fixtures, session token caching, self-healing cleanup, and failure screenshot/trace hooks.
8. [`features/e2e/cross_layer.feature`](file:///e:/Interview_Project/features/e2e/cross_layer.feature) — Cross-layer BDD scenarios proving seamless API + UI interplay.
9. [`.github/workflows/tests.yml`](file:///e:/Interview_Project/.github/workflows/tests.yml) — Production-ready CI pipeline with linting, smoke gates, and artifact capture.
10. [`README.md`](file:///e:/Interview_Project/README.md) — Comprehensive developer onboarding with Mermaid architecture diagrams.

---

## 2. Why Each Tool Was Chosen

| Tool | Purpose | Why This Choice Over Alternatives |
|------|---------|-----------------------------------|
| **Python 3.11+** | Primary Language | Fast startup, native type hinting, modern pattern matching, clean readable syntax. |
| **Playwright (Sync)** | Browser Automation | Superior reliability over Selenium. Web-first auto-waiting, native network interception, multi-context browser isolation, built-in trace viewer. |
| **Playwright `APIRequestContext`** | API Testing | Avoids adding third-party HTTP clients (`requests`/`httpx`). Shares cookies and browser network state natively for effortless E2E testing. |
| **pytest + pytest-bdd** | Test Runner & Gherkin | Industry standard. Native support for fixtures, parameterized runs, tags, and Allure reporting without the boilerplate of standalone Behave. |
| **jsonschema** | Contract Testing | Validates API response structures against Draft-07 schemas, catching backend contract breaking changes instantly. |
| **Ruff** | Linter & Formatter | 100x faster than Flake8/Black, enforcing clean code style and PEP 8 compliance automatically. |
| **Allure Framework** | Reporting | Rich interactive reports with embedded screenshots, step logs, execution timelines, and network payloads on failure. |

---

## 3. How Test Data and Cleanup Work on a Shared Demo

### The Problem
The target system (`automationintesting.online`) is a shared public demo environment that resets its database roughly every 10 minutes. Other external users and automated tests create and delete data concurrently.

### The Solution
1. **Never Depend on Seed Data**:
   Tests never assert hardcoded room counts (e.g. `assert len(rooms) == 3`). Tests create their own unique entities and assert structural properties.
2. **Deterministic Data Factories (`factories.py`)**:
   Every entity created gets an `AUTO_<timestamp>_<random>` prefix (e.g. `AUTO_1793693102`).
3. **API-First Cleanup Fixtures (`conftest.py`)**:
   `cleanup_rooms`, `cleanup_bookings`, and `cleanup_messages` fixtures collect created IDs and issue API `DELETE` calls during pytest teardown.
4. **Idempotent Cleanup**:
   Cleanup routines wrap deletions in `try...except` blocks; if the demo server reset midway through a test, the test suite does not fail on cleanup.
5. **State Restoration**:
   Tests that modify global configuration (e.g. `UI-033` Branding update) fetch the original configuration in `Given`, apply the test change, and restore the original state in `Teardown`.

---

## 4. How Flakiness is Handled (Zero-Sleep Policy)

- **No `time.sleep()`**:
  Arbitrary sleeps slow down test suites and fail unpredictably under CPU or network load.
- **Web-First Assertions (`expect(...)`)**:
  Playwright checks the DOM continuously until the expected state is met or the timeout expires.
- **Auto-Waiting Locators**:
  Locators wait for elements to be attached, visible, stable, and ready to receive pointer events before acting.
- **Transient Network Lag Resilience**:
  Navigation helper in `BasePage` defaults to `domcontentloaded` with an automatic fallback to `commit`, preventing Cloudflare reverse-proxy timeouts on slow networks.
- **Automatic Trace & Screenshot Capture**:
  On any test failure, Playwright saves a full-page PNG screenshot and a `.zip` execution trace showing DOM snapshots before and after every action.

---

## 5. What I Would Improve With More Time

1. **Dockerized Local Mock Environment**:
   Run the Restful Booker Platform backend locally via Docker Compose for offline CI execution without public internet dependency.
2. **Visual Regression Testing**:
   Integrate Playwright's native pixel-diffing (`expect(page).to_have_screenshot()`) for responsive layout testing.
3. **Automated OpenAPI / Swagger Code Generation**:
   Auto-generate client classes from OpenAPI specs when available.
4. **Parallel Sharding in GitHub Actions**:
   Split test execution across 4 parallel GitHub Actions matrix runners to reduce full suite execution time under 3 minutes.
