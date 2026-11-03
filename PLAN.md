# Restful Booker Platform: Automation Plan

## 1. Test Case Summary

### Counts by Sheet

| Sheet           | Total | P1 | P2 | P3 | Automate=Yes |
|-----------------|-------|----|----|----|--------------|
| UI Test Cases   |  34   | 13 | 14 |  7 |  34 (100%)   |
| API Test Cases  |  39   | 11 | 19 |  9 |  39 (100%)   |
| E2E Test Cases  |  10   |  4 |  4 |  2 |  10 (100%)   |
| **Total**       | **83**|**28**|**37**|**18**| **83** |

### Tag Distribution

| Tag         | UI | API | E2E |
|-------------|-----|-----|-----|
| @smoke      |  7  |  6  |  3  |
| @regression |  3  |  0  |  0  |
| @negative   |  9  | 11  |  1  |
| @boundary   |  4  |  0  |  0  |
| @security   |  1  |  3  |  1  |
| @e2e        |  6  |  0  | 10  |
| @contract   |  0  |  1  |  0  |
| @nfr        |  0  |  1  |  0  |

### Unconfirmed Assumptions (asterisked in manual sheet)

24 API test cases have asterisked expected results — these represent **status codes and behaviours to confirm in Phase 1 Discovery**:
- Auth errors: API-003 (401/403?), API-004/006 (4xx?)
- Room CRUD: API-010 (404?), API-011 (200/201?), API-012–015 (various)
- Booking CRUD: API-017 (200/201?), API-018–021, API-025–028
- Message/Report: API-028–029, API-032–033, API-035, API-037–038
- E2E-006: API returns 404 after room deleted via UI

---

## 2. Automation Scope Decision

### Automate All 83 — with these caveats:

| TC ID   | Flag | Reason |
|---------|------|--------|
| UI-034  | ⚠️ Partial | Responsive/mobile viewport: can automate with Playwright `set_viewport_size`, but assertions will be structural (no horizontal scroll), not visual pixel comparisons. Accept this trade-off. |
| UI-028  | ⚠️ Calendar | Admin booking calendar rendering depends on a datepicker component; locator strategy needs discovery. Mark as potentially fragile — retry strategy applied. |
| UI-032  | ⚠️ Report | Report page may have dynamic data from shared demo; assert structure not exact values. |
| API-039 | ⚠️ NFR | Response time is a soft threshold (2 s), not a hard SLA. Implemented as an `@xfail` soft assertion if over threshold on shared demo. |
| E2E-003 | ⚠️ Calendar | Same calendar risk as UI-028. |

All cases are marked `Automate = Yes` in the sheet, so none are excluded. The 5 flagged cases are automated with documented caveats.

---

## 3. Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     pytest-bdd (Gherkin runner)                      │
│  features/api/*.feature  features/ui/*.feature  features/e2e/*.feature│
└────────────────┬───────────────────┬───────────────────┬────────────┘
                 │                   │                   │
        ┌────────▼────────┐  ┌───────▼───────┐  ┌───────▼───────┐
        │  API Step Defs  │  │  UI Step Defs  │  │ E2E Step Defs │
        │  (tests/step_   │  │  (tests/step_  │  │ (tests/step_  │
        │  defs/api_steps)│  │  defs/ui_steps)│  │ defs/e2e_steps│
        └────────┬────────┘  └───────┬────────┘  └───────┬───────┘
                 │                   │                   │
     ┌───────────▼──────┐  ┌─────────▼──────────┐       │
     │   API Clients    │  │    Page Objects      │       │
     │  src/api/        │  │    src/pages/        │       │
     │  BaseClient      │  │    BasePage          │       │
     │  auth_api.py     │  │    home_page.py      │       │
     │  room_api.py     │  │    booking_panel.py  │       │
     │  booking_api.py  │  │    contact_form.py   │       │
     │  message_api.py  │  │    admin_login.py    │       │
     │  report_api.py   │  │    admin_rooms.py    │       │
     │  branding_api.py │  │    admin_messages.py │       │
     └──────────────────┘  └────────────────────┘       │
                 │                   │                   │
     ┌───────────▼───────────────────▼───────────────────▼──────────┐
     │                     Common Infrastructure                      │
     │  config/settings.py   src/data/factories.py                   │
     │  src/utils/logger.py  src/utils/waits.py  src/utils/assertions │
     │  src/models/schemas/  tests/conftest.py                        │
     │  Playwright APIRequestContext  |  Playwright Browser           │
     └────────────────────────────────────────────────────────────────┘
```

### Key Design Decisions (preview; full detail in docs/DECISIONS.md)

1. **pytest-bdd not Behave**: Skill file mandates pytest-bdd. It integrates with pytest fixtures and allure natively.
2. **Playwright APIRequestContext for API**: Not `requests`. Same tool for UI and API avoids dual dependency; shares session context.
3. **Page Object Model**: No raw locators inside step definitions. Locators live only in page objects.
4. **Session-scoped auth token**: One login per test run; reused via `@pytest.fixture(scope="session")`.
5. **Shared `context` dict**: Step-to-step state via a function-scoped dict fixture, not globals.
6. **AUTO_ prefix + timestamp + random**: All created data is unique and identifiable for cleanup.

---

## 4. Folder Layout (per SKILL.md)

```
e:\Interview_Project\
├── .agent/skills/rbp-automation/SKILL.md        (project rules — read-only)
├── .github/
│   └── workflows/
│       └── tests.yml
├── config/
│   └── settings.py                              env-driven configuration
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── base_client.py
│   │   ├── auth_api.py
│   │   ├── room_api.py
│   │   ├── booking_api.py
│   │   ├── message_api.py
│   │   ├── report_api.py
│   │   └── branding_api.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py
│   │   ├── home_page.py
│   │   ├── booking_panel.py
│   │   ├── contact_form.py
│   │   ├── admin_login_page.py
│   │   ├── admin_rooms_page.py
│   │   ├── admin_messages_page.py
│   │   ├── admin_report_page.py
│   │   └── admin_branding_page.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── room.py
│   │   ├── booking.py
│   │   └── message.py
│   ├── schemas/
│   │   ├── room_schema.json
│   │   ├── booking_schema.json
│   │   └── message_schema.json
│   ├── data/
│   │   ├── __init__.py
│   │   └── factories.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       ├── waits.py
│       └── assertions.py
├── features/
│   ├── api/
│   │   ├── auth.feature
│   │   ├── rooms.feature
│   │   ├── bookings.feature
│   │   ├── messages.feature
│   │   ├── report.feature
│   │   └── branding.feature
│   ├── ui/
│   │   ├── home.feature
│   │   ├── booking.feature
│   │   ├── contact.feature
│   │   ├── admin_auth.feature
│   │   ├── admin_rooms.feature
│   │   ├── admin_messages.feature
│   │   ├── admin_report.feature
│   │   ├── admin_branding.feature
│   │   └── responsive.feature
│   └── e2e/
│       └── cross_layer.feature
├── tests/
│   ├── conftest.py
│   ├── step_defs/
│   │   ├── __init__.py
│   │   ├── common_steps.py
│   │   ├── api_steps/
│   │   │   ├── __init__.py
│   │   │   ├── auth_steps.py
│   │   │   ├── room_steps.py
│   │   │   ├── booking_steps.py
│   │   │   ├── message_steps.py
│   │   │   ├── report_steps.py
│   │   │   └── branding_steps.py
│   │   ├── ui_steps/
│   │   │   ├── __init__.py
│   │   │   ├── home_steps.py
│   │   │   ├── booking_steps.py
│   │   │   ├── contact_steps.py
│   │   │   ├── admin_auth_steps.py
│   │   │   ├── admin_rooms_steps.py
│   │   │   └── admin_messages_steps.py
│   │   └── e2e_steps/
│   │       ├── __init__.py
│   │       └── cross_layer_steps.py
│   ├── test_api.py
│   ├── test_ui.py
│   └── test_e2e.py
├── docs/
│   ├── RestfulBooker_Manual_Test_Cases.xlsx
│   ├── DECISIONS.md
│   ├── DISCOVERY.md                 (Phase 1 output)
│   ├── TRACEABILITY.md              (Phase 7 output)
│   ├── WALKTHROUGH.md               (Phase 7 output)
│   └── discovery_samples/           (Phase 1 raw JSON)
├── scripts/
│   └── discover.py                  (Phase 1 discovery script)
├── reports/
│   └── allure/                      (gitignored)
├── PLAN.md
├── PROGRESS.md
├── README.md
├── requirements.txt
├── pyproject.toml
├── pytest.ini
├── .env.example
└── .gitignore
```

---

## 5. Phases and Timeline

| Phase | Name              | Key Deliverables                                     |
|-------|-------------------|------------------------------------------------------|
| 0     | Understand & Plan | PLAN.md, PROGRESS.md, DECISIONS.md (skeleton)       |
| 1     | Discovery         | discover.py, DISCOVERY.md, discovery_samples/        |
| 2     | Scaffold          | requirements.txt, pyproject.toml, pytest.ini, .env   |
| 3     | Core Framework    | config, src/ layer, conftest.py, smoke test passes   |
| 4     | API Features      | features/api/*.feature + step defs; `pytest -m api`  |
| 5     | UI Features       | features/ui/*.feature + step defs; `pytest -m ui`    |
| 6     | E2E Features      | features/e2e/*.feature + step defs; `pytest -m e2e`  |
| 7     | Reporting & CI    | Allure, GitHub Actions, TRACEABILITY.md, README.md   |
| 8     | Final Verify      | Two full runs, EXECUTION_REPORT.md, reviewer guide   |

---

## 6. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Demo resets every ~10 min | High | Medium | Session-scoped token refresh; API-first cleanup; no seed data dependency |
| Other users create/delete data | High | Medium | Assert structure/types, not exact counts; use unique `AUTO_` prefix to identify own data |
| Flaky UI calendar interactions | Medium | High | Playwright auto-wait; network idle; retry on failure (1 rerun UI only); xfail with reason if persistently broken |
| API schema changes (public demo) | Low | High | jsonschema contract tests in CI catch regressions early |
| Rate limiting / IP blocks | Low | Medium | Low parallelism (2 workers max); no loops; polite request volume |
| Branding left dirty after test | Medium | Low | Always restore in fixture teardown; teardown survives demo reset |
| Status codes differ from sheet | High | Low | All asterisked cases confirmed in Phase 1 discovery before writing assertions |
| Windows path issues | Low | Low | All paths use os.path / pathlib in Python code |

