---
name: rbp-automation
description: Rules, conventions and commands for the Restful Booker Platform UI + API test framework (Python, Playwright, pytest-bdd). Read before creating or editing any file in this project.
---

# Restful Booker Platform Automation: Project Skill

## 1. Target system
- UI: https://automationintesting.online
- API base: https://automationintesting.online/api  (services: auth, room, booking, message, report, branding)
- Admin credentials (public demo): `admin` / `password`
- It is a shared public demo. Data resets about every 10 minutes. Other people use it.
- Never hard-code the base URL, credentials or timeouts. Read them from `.env` through `config/settings.py`.

## 2. Stack (do not substitute)
- Python 3.11+
- `pytest`, `pytest-playwright` (Playwright sync API), `pytest-bdd` (Gherkin; Cucumber itself is not Python)
- API calls use Playwright `APIRequestContext` (not `requests`)
- `jsonschema` for contract checks, `python-dotenv`, `faker` for unique data
- `allure-pytest` for reports, `pytest-xdist` optional, `ruff` for lint/format

## 3. Folder layout
```
.
├── .agent/skills/rbp-automation/SKILL.md   (this file)
├── config/settings.py                       env-driven config
├── src/
│   ├── api/            base_client.py, auth_api.py, room_api.py, booking_api.py, message_api.py, report_api.py, branding_api.py
│   ├── pages/          base_page.py, home_page.py, booking_panel.py, contact_form.py, admin_login_page.py, admin_rooms_page.py, admin_messages_page.py, admin_report_page.py, admin_branding_page.py
│   ├── models/         pydantic or dataclass payloads, JSON schemas in schemas/
│   ├── data/           factories.py (unique data builders)
│   └── utils/          logger.py, waits.py, assertions.py
├── features/
│   ├── api/            *.feature
│   ├── ui/             *.feature
│   └── e2e/            *.feature
├── tests/
│   ├── conftest.py     fixtures + hooks
│   ├── step_defs/      api_steps/, ui_steps/, e2e_steps/, common_steps.py
│   ├── test_api.py     scenarios("../features/api")
│   ├── test_ui.py      scenarios("../features/ui")
│   └── test_e2e.py     scenarios("../features/e2e")
├── docs/               manual test cases xlsx, DISCOVERY.md, DECISIONS.md, TRACEABILITY.md, WALKTHROUGH.md
├── .github/workflows/tests.yml
├── pytest.ini, pyproject.toml, requirements.txt, .env.example, .gitignore, README.md
```

## 4. Naming and traceability
- Every scenario name starts with its manual TC ID from `docs/RestfulBooker_Manual_Test_Cases.xlsx`, e.g. `Scenario: UI-004 Create booking with valid data`.
- Tags come from the Tags column of the sheet: `@ui @api @e2e @smoke @regression @negative @boundary @security`.
- Register every tag in `pytest.ini` under `markers`.
- Maintain `docs/TRACEABILITY.md`: TC ID, feature file, scenario, automated (yes/no), reason if no.

## 5. Coding rules
- Page Object Model: page classes hold locators and actions; no assertions inside page objects except small `expect_*` helpers.
- API clients return the response object; steps assert. One client class per service, sharing a `BaseClient`.
- Locator priority: `get_by_role`, `get_by_label`, `get_by_placeholder`, `get_by_text`, stable `id`/`data-testid`, then CSS. No XPath unless unavoidable (explain in a comment).
- No `time.sleep` and no `wait_for_timeout`. Use Playwright auto-waiting and `expect(...)` web-first assertions.
- Steps are reusable and parameterised. Put steps used by more than one feature in `common_steps.py`.
- Shared state between steps goes in a `context` dict fixture, never in globals.
- Type hints and short docstrings on public functions. `ruff` must pass.
- Do not duplicate selectors, URLs or payloads across files.

## 6. Test data rules
- Every created entity gets a unique name via `factories.py` (prefix `AUTO_` + timestamp + short random).
- Create your own data inside the test or fixture. Never depend on seed data surviving.
- Clean up in fixture teardown or an `After` hook, by API where possible. Cleanup must not fail the test if the demo has already reset.
- Do not assert exact seed values (names, counts). Assert structure, types and relationships.
- Restore any shared setting you change (branding) in teardown.

## 7. Auth
- API token: login through `auth_api`, cache per session in a session-scoped fixture.
- UI admin: reuse the authenticated state (cookie or storage state) where it works; keep one UI test that logs in through the form.

## 8. Reliability on a shared public demo
- Session-level health check (auth and booking actuator health, home page 200). Skip the run with a clear message if the site is down.
- Retries: at most 1 rerun for UI (`--reruns 1`), none for API.
- Keep parallelism low (2 workers max). Be polite to the public site.
- Capture screenshot, trace and video on UI failure. Attach request/response to Allure on API failure.

## 9. Things that must be confirmed by discovery, not assumed
Status codes, field length limits, exact API paths and request/response shapes. Record them in `docs/DISCOVERY.md` and use those values. If the observed behaviour differs from the manual sheet, the observed behaviour wins and the difference is logged in `docs/DISCOVERY.md`.

## 10. Commands
```
pip install -r requirements.txt
playwright install chromium
pytest -m smoke                      # smoke
pytest -m api                        # API only
pytest -m ui --headed                # UI, visible browser
pytest -m "e2e or smoke" -n 2
pytest --alluredir=reports/allure && allure serve reports/allure
ruff check . && ruff format .
```

## 11. Definition of done for any task
1. Code is linted and formatted.
2. The affected tests were actually run and the result was reported honestly (pass, fail and why).
3. TRACEABILITY.md and DECISIONS.md updated.
4. No secrets or hard-coded URLs committed.
5. Progress logged in `PROGRESS.md`.

## 12. Never
- Never invent results, status codes or pass counts. Report what actually ran.
- Never touch anything outside the target site's documented demo behaviour, and never run load or abuse traffic.
- Never skip a failing test silently. Fix it, or mark `xfail` with a written reason.
