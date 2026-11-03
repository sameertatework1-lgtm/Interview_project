from pathlib import Path

import openpyxl

wb = openpyxl.load_workbook(r"docs/RestfulBooker_Manual_Test_Cases.xlsx")

output_lines = [
    "# Requirements & Test Traceability Matrix",
    "",
    "> Complete mapping from manual test cases (`docs/RestfulBooker_Manual_Test_Cases.xlsx`) to automated Gherkin scenarios and step definitions.",
    "",
    "| TC ID | Module | Title | Priority | Automated | Feature File | Scenario Name | Status / Note |",
    "|-------|--------|-------|----------|-----------|--------------|---------------|---------------|",
]

feature_mapping = {
    # UI
    "UI-001": ("features/ui/home.feature", "UI-001 Home page loads with core sections"),
    "UI-002": ("features/ui/home.feature", "UI-002 Room cards show name type price and features"),
    "UI-003": ("features/ui/booking.feature", "UI-003 Open booking panel shows calendar and form"),
    "UI-004": (
        "features/ui/booking.feature",
        "UI-004 Create booking with valid data shows success",
    ),
    "UI-005": (
        "features/ui/booking.feature",
        "UI-005 Submit booking with all fields empty shows validation errors",
    ),
    "UI-006": ("features/ui/booking.feature", "UI-006 Invalid email format shows email error"),
    "UI-007": (
        "features/ui/booking.feature",
        "UI-007 Phone number below minimum length shows error",
    ),
    "UI-008": ("features/ui/booking.feature", "UI-008 Name length boundaries"),
    "UI-009": ("features/ui/booking.feature", "UI-009 Cancel booking form closes panel"),
    "UI-010": ("features/ui/booking.feature", "UI-010 Overlapping dates are rejected"),
    "UI-011": (
        "features/ui/contact.feature",
        "UI-011 Submit valid contact form shows confirmation",
    ),
    "UI-012": (
        "features/ui/contact.feature",
        "UI-012 Submit empty contact form shows validation errors",
    ),
    "UI-013": (
        "features/ui/contact.feature",
        "UI-013 Message shorter than minimum shows length error",
    ),
    "UI-014": (
        "features/ui/contact.feature",
        "UI-014 Invalid email format in contact form shows error",
    ),
    "UI-015": ("features/ui/contact.feature", "UI-015 Subject too short shows length error"),
    "UI-016": (
        "features/ui/admin_auth.feature",
        "UI-016 Admin login with valid credentials shows dashboard",
    ),
    "UI-017": ("features/ui/admin_auth.feature", "UI-017 Login with wrong password shows error"),
    "UI-018": ("features/ui/admin_auth.feature", "UI-018 Login with empty credentials shows error"),
    "UI-019": ("features/ui/admin_auth.feature", "UI-019 Logout returns to home page"),
    "UI-020": (
        "features/ui/admin_auth.feature",
        "UI-020 Direct access to admin URL without login shows login form",
    ),
    "UI-021": ("features/ui/admin_auth.feature", "UI-021 Session persists after page refresh"),
    "UI-022": (
        "features/ui/admin_rooms.feature",
        "UI-022 Create room with valid data appears in list",
    ),
    "UI-023": (
        "features/ui/admin_rooms.feature",
        "UI-023 Create room with missing name shows validation error",
    ),
    "UI-024": (
        "features/ui/admin_rooms.feature",
        "UI-024 Create room with invalid price shows error",
    ),
    "UI-025": ("features/ui/admin_rooms.feature", "UI-025 Edit room price is saved"),
    "UI-026": ("features/ui/admin_rooms.feature", "UI-026 Delete room removes it from list"),
    "UI-027": ("features/ui/admin_rooms.feature", "UI-027 Room features are saved and shown"),
    "UI-028": ("features/ui/admin_rooms.feature", "UI-028 Booking appears in admin calendar"),
    "UI-029": (
        "features/ui/admin_messages.feature",
        "UI-029 Contact message arrives in admin inbox",
    ),
    "UI-030": (
        "features/ui/admin_messages.feature",
        "UI-030 Open and read a message shows details",
    ),
    "UI-031": (
        "features/ui/admin_messages.feature",
        "UI-031 Delete a message removes it from list",
    ),
    "UI-032": ("features/ui/admin_messages.feature", "UI-032 Report page shows occupancy calendar"),
    "UI-033": (
        "features/ui/admin_messages.feature",
        "UI-033 Update branding details show on home page",
    ),
    "UI-034": (
        "features/ui/admin_messages.feature",
        "UI-034 Home page renders on mobile viewport without horizontal scroll",
    ),
    # API
    "API-001": ("features/api/auth.feature", "API-001 Auth health check returns UP"),
    "API-002": ("features/api/auth.feature", "API-002 Login with valid credentials returns token"),
    "API-003": ("features/api/auth.feature", "API-003 Login with invalid credentials is rejected"),
    "API-004": (
        "features/api/auth.feature",
        "API-004 Login with missing password field returns error",
    ),
    "API-005": ("features/api/auth.feature", "API-005 Validate a valid token succeeds"),
    "API-006": ("features/api/auth.feature", "API-006 Validate an invalid token is rejected"),
    "API-007": ("features/api/auth.feature", "API-007 Logout invalidates the token"),
    "API-008": ("features/api/rooms.feature", "API-008 List rooms returns 200 with rooms array"),
    "API-009": ("features/api/rooms.feature", "API-009 Get room by id returns the room"),
    "API-010": ("features/api/rooms.feature", "API-010 Get non-existent room returns 404"),
    "API-011": ("features/api/rooms.feature", "API-011 Create room with valid token returns 200"),
    "API-012": ("features/api/rooms.feature", "API-012 Create room without token is rejected"),
    "API-013": ("features/api/rooms.feature", "API-013 Create room with missing name returns 400"),
    "API-014": ("features/api/rooms.feature", "API-014 Update room changes the price"),
    "API-015": ("features/api/rooms.feature", "API-015 Delete room then GET returns 404"),
    "API-016": ("features/api/rooms.feature", "API-016 Room response matches JSON schema"),
    "API-017": (
        "features/api/bookings.feature",
        "API-017 Create booking with valid data returns success",
    ),
    "API-018": (
        "features/api/bookings.feature",
        "API-018 Create booking missing lastname returns 400",
    ),
    "API-019": (
        "features/api/bookings.feature",
        "API-019 Booking with checkout before checkin is rejected",
    ),
    "API-020": ("features/api/bookings.feature", "API-020 Overlapping booking is rejected"),
    "API-021": ("features/api/bookings.feature", "API-021 Booking with invalid email returns 400"),
    "API-022": (
        "features/api/bookings.feature",
        "API-022 List bookings by room id returns bookings",
    ),
    "API-023": ("features/api/bookings.feature", "API-023 Get booking by id returns correct data"),
    "API-024": (
        "features/api/bookings.feature",
        "API-024 Booking summary by room returns date ranges",
    ),
    "API-025": ("features/api/bookings.feature", "API-025 Update booking changes dates"),
    "API-026": ("features/api/bookings.feature", "API-026 Delete booking then GET returns 404"),
    "API-027": ("features/api/bookings.feature", "API-027 Get booking without token returns 401"),
    "API-028": ("features/api/messages.feature", "API-028 Send contact message returns success"),
    "API-029": (
        "features/api/messages.feature",
        "API-029 Send message with short description returns 400",
    ),
    "API-030": (
        "features/api/messages.feature",
        "API-030 List messages as admin returns the sent message",
    ),
    "API-031": (
        "features/api/messages.feature",
        "API-031 Get message by id returns correct fields",
    ),
    "API-032": ("features/api/messages.feature", "API-032 Mark message as read sets read flag"),
    "API-033": ("features/api/messages.feature", "API-033 Delete message then GET returns 404"),
    "API-034": ("features/api/report.feature", "API-034 Get report as admin returns 200"),
    "API-035": ("features/api/report.feature", "API-035 Get report without token returns 401"),
    "API-036": (
        "features/api/branding.feature",
        "API-036 Get branding returns 200 with name and contact",
    ),
    "API-037": (
        "features/api/branding.feature",
        "API-037 Update branding name as admin then restore",
    ),
    "API-038": (
        "features/api/branding.feature",
        "API-038 Unsupported method on room list returns 405",
    ),
    "API-039": (
        "features/api/branding.feature",
        "API-039 Room list responds within 2 seconds with JSON content-type",
    ),
    # E2E
    "E2E-001": (
        "features/e2e/cross_layer.feature",
        "E2E-001 Room created via API shows on UI home page",
    ),
    "E2E-002": ("features/e2e/cross_layer.feature", "E2E-002 Booking made on UI is stored in API"),
    "E2E-003": (
        "features/e2e/cross_layer.feature",
        "E2E-003 Booking created via API shows in admin calendar",
    ),
    "E2E-004": ("features/e2e/cross_layer.feature", "E2E-004 API-booked dates conflict in UI"),
    "E2E-005": (
        "features/e2e/cross_layer.feature",
        "E2E-005 Contact message from UI visible via API",
    ),
    "E2E-006": (
        "features/e2e/cross_layer.feature",
        "E2E-006 Room deleted in admin UI returns 404 on API",
    ),
    "E2E-007": ("features/e2e/cross_layer.feature", "E2E-007 Price update via API reflected on UI"),
    "E2E-008": ("features/e2e/cross_layer.feature", "E2E-008 Full lifecycle with cleanup"),
    "E2E-009": (
        "features/e2e/cross_layer.feature",
        "E2E-009 Branding update via API reflected on UI then restored",
    ),
    "E2E-010": ("features/e2e/cross_layer.feature", "E2E-010 UI logout invalidates the API token"),
}

for sheet_name in ["UI Test Cases", "API Test Cases", "E2E Test Cases"]:
    ws = wb[sheet_name]
    headers = [cell.value for cell in ws[1]]
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        tc = dict(zip(headers, row, strict=False))
        tc_id = tc["TC ID"]
        module = tc["Module"]
        title = tc["Test Title"]
        prio = tc["Priority"]
        feat, scen = feature_mapping.get(tc_id, ("-", "-"))
        note = "Automated"
        if tc_id == "API-001":
            note = "Automated (xfail - live actuator 500)"
        elif tc_id == "API-039":
            note = "Automated (NFR soft assertion)"
        elif tc_id == "UI-034":
            note = "Automated (viewport structural assertion)"
        elif tc_id == "E2E-010":
            note = "Automated (xfail - session cookie decoupling)"
        elif tc_id == "UI-008":
            note = "Automated (boundary validation)"
        output_lines.append(
            f"| {tc_id} | {module} | {title} | {prio} | Yes | `{feat}` | {scen} | {note} |"
        )

Path("docs/TRACEABILITY.md").write_text("\n".join(output_lines), encoding="utf-8")
print("TRACEABILITY.md generated successfully!")
