# Test Automation Framework Prompt Chain

This document records the exact, structured prompt chain utilized to design, scaffold, implement, and verify the Restful Booker Platform Test Automation Framework. Designed for client review to demonstrate professional SDET engineering rigor.

---

## Prompt 1: Phase 0 — Understand and Plan
```text
Role: Senior SDET (8+ years experience).
Project: Restful Booker Platform Automation Framework.
Inputs: Read .agent/skills/rbp-automation/SKILL.md as binding rules. Read docs/RestfulBooker_Manual_Test_Cases.xlsx across all sheets.
Objectives:
1. Parse and summarize manual test cases by sheet, priority, and tags.
2. Select cases to automate, documenting automation-fit caveats (e.g., visual calendar drags, NFRs).
3. Produce PLAN.md covering architecture, strict folder structure, phase roadmap, and risk mitigations (shared environment, resets).
4. Do not write test code until planning passes review.
```

---

## Prompt 2: Phase 1 — Live System Discovery & Contract Verification
```text
Role: SDET Engineer.
Context: The manual test sheet contains unconfirmed assumptions (starred status codes, payload shapes, routes).
Objectives:
1. Write scripts/discover.py using Playwright sync API to probe all live services: /auth, /room, /booking, /message, /report, /branding.
2. Probe negative cases: unauthenticated access, missing fields, unknown IDs, overlapping bookings, boundary payloads.
3. Save raw HTTP responses under docs/discovery_samples/.
4. Produce docs/DISCOVERY.md documenting confirmed routes, status codes, auth headers (token cookies), and differences from the manual sheet.
```

---

## Prompt 3: Phase 2 — Project Scaffolding & Toolchain Setup
```text
Role: Automation Architect.
Objectives:
1. Initialize project structure per SKILL.md specification.
2. Create requirements.txt with pinned dependencies (Playwright, pytest, pytest-bdd, jsonschema, python-dotenv, Faker, ruff, allure-pytest).
3. Configure pyproject.toml (Ruff linting & formatting, line-length=100) and pytest.ini (markers, test paths, strict markers).
4. Provide .env.example, .env, and .gitignore.
5. Verify clean package installation and pytest test collection without errors.
```

---

## Prompt 4: Phase 3 — Core Framework Architecture
```text
Role: Senior SDET.
Objectives:
1. Build config/settings.py reading environment variables with secure defaults.
2. Implement src/api/base_client.py wrapping Playwright APIRequestContext with structured logging and Allure attachments.
3. Create individual API service clients: AuthAPI, RoomAPI, BookingAPI, MessageAPI, ReportAPI, BrandingAPI.
4. Define JSON schemas in src/schemas/ for contract validation.
5. Implement src/data/factories.py with unique AUTO_ prefixes and random timestamp suffixes to guarantee non-colliding test data.
6. Build Page Object Model: src/pages/base_page.py with resilient navigation, plus individual page objects.
7. Configure tests/conftest.py with session health check, token caching, failure screenshot/trace capture, and cleanup hooks.
8. Validate with a smoke scenario passing end-to-end.
```

---

## Prompt 5: Phase 4 — API BDD Feature Implementation
```text
Role: Test Automation Engineer.
Objectives:
1. Author Gherkin .feature files under features/api/ covering all Automate=Yes manual cases.
2. Implement step definitions under tests/step_defs/api_steps/ and common_steps.py.
3. Assert status codes, JSON schemas, payload fields, and error structures based on DISCOVERY.md findings.
4. Flag known demo environment defects (e.g. actuator health 500) using pytest xfail with explicit rationale.
5. Verify execution with pytest -m api.
```

---

## Prompt 6: Phase 5 — UI BDD Feature Implementation
```text
Role: Front-End Automation SDET.
Objectives:
1. Author Gherkin .feature files under features/ui/ (home, booking, contact, admin auth, admin rooms, admin messages).
2. Implement UI step definitions under tests/step_defs/ui_steps/ strictly using Page Object methods (zero raw locators in steps).
3. Handle single-page app reactivity and modal states without arbitrary sleeps (relying on Playwright auto-waiting and web-first assertions).
4. Verify execution with pytest -m ui.
```

---

## Prompt 7: Phase 6 — End-to-End Cross-Layer Integration
```text
Role: Full-Stack SDET.
Objectives:
1. Author cross-layer scenarios in features/e2e/ combining API precondition setup with UI validation, and UI action with API verification.
2. Implement tests/step_defs/e2e_steps/ with guaranteed resource cleanup (cleanup_rooms, cleanup_bookings fixtures).
3. Validate suite execution with pytest -m e2e.
```

---

## Prompt 8: Phase 7 — CI/CD, Traceability & Code Quality
```text
Role: Lead SDET / DevOps.
Objectives:
1. Configure .github/workflows/tests.yml with multi-event triggers (push, PR, schedule, manual dispatch), artifact archiving, and retries.
2. Generate docs/TRACEABILITY.md mapping every manual TC ID to its automated Gherkin scenario and status.
3. Verify zero ruff lint errors and enforce formatting.
4. Complete comprehensive README.md and docs/WALKTHROUGH.md.
```

---

## Prompt 9: Phase 8 — Final Verification & Reviewer Packaging
```text
Role: SDET Reviewer.
Objectives:
1. Execute verification runs across API, UI, and E2E suites.
2. Audit codebase against hard quality gates:
   - Zero hard-coded URLs (environment driven).
   - Zero time.sleep calls across src/ and tests/ (Playwright smart waiting only).
   - Zero plain-text credentials or secrets.
   - Every scenario starts with its manual TC ID.
   - Every tag is registered in pytest.ini.
3. Produce docs/EXECUTION_REPORT.md and client presentation guide.
```

