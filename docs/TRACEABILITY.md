# Requirements & Test Traceability Matrix

> Complete mapping from manual test cases (`docs/RestfulBooker_Manual_Test_Cases.xlsx`) to automated Gherkin scenarios and step definitions.

| TC ID | Module | Title | Priority | Automated | Feature File | Scenario Name | Status / Note |
|-------|--------|-------|----------|-----------|--------------|---------------|---------------|
| UI-001 | Home | Home page loads with core sections | P1 | Yes | `features/ui/home.feature` | UI-001 Home page loads with core sections | Automated |
| UI-002 | Home | Room cards show name/type, price and features | P2 | Yes | `features/ui/home.feature` | UI-002 Room cards show name type price and features | Automated |
| UI-003 | Booking | Open booking panel for a room | P1 | Yes | `features/ui/booking.feature` | UI-003 Open booking panel shows calendar and form | Automated |
| UI-004 | Booking | Create booking with valid data | P1 | Yes | `features/ui/booking.feature` | UI-004 Create booking with valid data shows success | Automated |
| UI-005 | Booking | Submit booking with all fields empty | P1 | Yes | `features/ui/booking.feature` | UI-005 Submit booking with all fields empty shows validation errors | Automated |
| UI-006 | Booking | Invalid email format | P2 | Yes | `features/ui/booking.feature` | UI-006 Invalid email format shows email error | Automated |
| UI-007 | Booking | Phone number below minimum length | P2 | Yes | `features/ui/booking.feature` | UI-007 Phone number below minimum length shows error | Automated |
| UI-008 | Booking | Name length boundaries | P2 | Yes | `features/ui/booking.feature` | UI-008 Name length boundaries | Automated (boundary validation) |
| UI-009 | Booking | Cancel booking form | P3 | Yes | `features/ui/booking.feature` | UI-009 Cancel booking form closes panel | Automated |
| UI-010 | Booking | Overlapping dates rejected | P1 | Yes | `features/ui/booking.feature` | UI-010 Overlapping dates are rejected | Automated |
| UI-011 | Contact | Submit valid contact form | P1 | Yes | `features/ui/contact.feature` | UI-011 Submit valid contact form shows confirmation | Automated |
| UI-012 | Contact | Submit empty contact form | P1 | Yes | `features/ui/contact.feature` | UI-012 Submit empty contact form shows validation errors | Automated |
| UI-013 | Contact | Message shorter than minimum | P2 | Yes | `features/ui/contact.feature` | UI-013 Message shorter than minimum shows length error | Automated |
| UI-014 | Contact | Invalid email format | P2 | Yes | `features/ui/contact.feature` | UI-014 Invalid email format in contact form shows error | Automated |
| UI-015 | Contact | Subject too short | P3 | Yes | `features/ui/contact.feature` | UI-015 Subject too short shows length error | Automated |
| UI-016 | Admin Auth | Admin login with valid credentials | P1 | Yes | `features/ui/admin_auth.feature` | UI-016 Admin login with valid credentials shows dashboard | Automated |
| UI-017 | Admin Auth | Login with wrong password | P1 | Yes | `features/ui/admin_auth.feature` | UI-017 Login with wrong password shows error | Automated |
| UI-018 | Admin Auth | Login with empty credentials | P2 | Yes | `features/ui/admin_auth.feature` | UI-018 Login with empty credentials shows error | Automated |
| UI-019 | Admin Auth | Logout | P1 | Yes | `features/ui/admin_auth.feature` | UI-019 Logout returns to home page | Automated |
| UI-020 | Admin Auth | Direct access to admin URL without login | P2 | Yes | `features/ui/admin_auth.feature` | UI-020 Direct access to admin URL without login shows login form | Automated |
| UI-021 | Admin Auth | Session persists after page refresh | P3 | Yes | `features/ui/admin_auth.feature` | UI-021 Session persists after page refresh | Automated |
| UI-022 | Admin Rooms | Create room with valid data | P1 | Yes | `features/ui/admin_rooms.feature` | UI-022 Create room with valid data appears in list | Automated |
| UI-023 | Admin Rooms | Create room with missing mandatory data | P2 | Yes | `features/ui/admin_rooms.feature` | UI-023 Create room with missing name shows validation error | Automated |
| UI-024 | Admin Rooms | Create room with invalid price | P2 | Yes | `features/ui/admin_rooms.feature` | UI-024 Create room with invalid price shows error | Automated |
| UI-025 | Admin Rooms | Edit room details | P2 | Yes | `features/ui/admin_rooms.feature` | UI-025 Edit room price is saved | Automated |
| UI-026 | Admin Rooms | Delete room | P2 | Yes | `features/ui/admin_rooms.feature` | UI-026 Delete room removes it from list | Automated |
| UI-027 | Admin Rooms | Room features persist | P3 | Yes | `features/ui/admin_rooms.feature` | UI-027 Room features are saved and shown | Automated |
| UI-028 | Admin Bookings | Booking appears in admin calendar | P1 | Yes | `features/ui/admin_rooms.feature` | UI-028 Booking appears in admin calendar | Automated |
| UI-029 | Admin Messages | Contact message arrives in admin inbox | P1 | Yes | `features/ui/admin_messages.feature` | UI-029 Contact message arrives in admin inbox | Automated |
| UI-030 | Admin Messages | Open and read a message | P2 | Yes | `features/ui/admin_messages.feature` | UI-030 Open and read a message shows details | Automated |
| UI-031 | Admin Messages | Delete a message | P2 | Yes | `features/ui/admin_messages.feature` | UI-031 Delete a message removes it from list | Automated |
| UI-032 | Admin Report | Report page shows occupancy | P3 | Yes | `features/ui/admin_messages.feature` | UI-032 Report page shows occupancy calendar | Automated |
| UI-033 | Admin Branding | Update branding details | P3 | Yes | `features/ui/admin_messages.feature` | UI-033 Update branding details show on home page | Automated |
| UI-034 | Responsive | Home page renders on mobile viewport | P3 | Yes | `features/ui/admin_messages.feature` | UI-034 Home page renders on mobile viewport without horizontal scroll | Automated (viewport structural assertion) |
| API-001 | Auth | Auth health check | P1 | Yes | `features/api/auth.feature` | API-001 Auth health check returns UP | Automated (xfail - live actuator 500) |
| API-002 | Auth | Login with valid credentials | P1 | Yes | `features/api/auth.feature` | API-002 Login with valid credentials returns token | Automated |
| API-003 | Auth | Login with invalid credentials | P1 | Yes | `features/api/auth.feature` | API-003 Login with invalid credentials is rejected | Automated |
| API-004 | Auth | Login with missing field | P2 | Yes | `features/api/auth.feature` | API-004 Login with missing password field returns error | Automated |
| API-005 | Auth | Validate a valid token | P2 | Yes | `features/api/auth.feature` | API-005 Validate a valid token succeeds | Automated |
| API-006 | Auth | Validate invalid token | P2 | Yes | `features/api/auth.feature` | API-006 Validate an invalid token is rejected | Automated |
| API-007 | Auth | Logout invalidates token | P2 | Yes | `features/api/auth.feature` | API-007 Logout invalidates the token | Automated |
| API-008 | Room | List rooms | P1 | Yes | `features/api/rooms.feature` | API-008 List rooms returns 200 with rooms array | Automated |
| API-009 | Room | Get room by id | P1 | Yes | `features/api/rooms.feature` | API-009 Get room by id returns the room | Automated |
| API-010 | Room | Get non-existent room | P2 | Yes | `features/api/rooms.feature` | API-010 Get non-existent room returns 404 | Automated |
| API-011 | Room | Create room with valid token | P1 | Yes | `features/api/rooms.feature` | API-011 Create room with valid token returns 200 | Automated |
| API-012 | Room | Create room without token | P1 | Yes | `features/api/rooms.feature` | API-012 Create room without token is rejected | Automated |
| API-013 | Room | Create room with invalid payload | P2 | Yes | `features/api/rooms.feature` | API-013 Create room with missing name returns 400 | Automated |
| API-014 | Room | Update room | P2 | Yes | `features/api/rooms.feature` | API-014 Update room changes the price | Automated |
| API-015 | Room | Delete room | P2 | Yes | `features/api/rooms.feature` | API-015 Delete room then GET returns 404 | Automated |
| API-016 | Room | Room response schema contract | P2 | Yes | `features/api/rooms.feature` | API-016 Room response matches JSON schema | Automated |
| API-017 | Booking | Create booking (public) | P1 | Yes | `features/api/bookings.feature` | API-017 Create booking with valid data returns success | Automated |
| API-018 | Booking | Create booking missing required field | P1 | Yes | `features/api/bookings.feature` | API-018 Create booking missing lastname returns 400 | Automated |
| API-019 | Booking | Checkout date before checkin | P2 | Yes | `features/api/bookings.feature` | API-019 Booking with checkout before checkin is rejected | Automated |
| API-020 | Booking | Overlapping booking | P1 | Yes | `features/api/bookings.feature` | API-020 Overlapping booking is rejected | Automated |
| API-021 | Booking | Invalid email/phone format | P2 | Yes | `features/api/bookings.feature` | API-021 Booking with invalid email returns 400 | Automated |
| API-022 | Booking | Get bookings by room id (admin) | P2 | Yes | `features/api/bookings.feature` | API-022 List bookings by room id returns bookings | Automated |
| API-023 | Booking | Get booking by id | P2 | Yes | `features/api/bookings.feature` | API-023 Get booking by id returns correct data | Automated |
| API-024 | Booking | Booking summary by room | P3 | Yes | `features/api/bookings.feature` | API-024 Booking summary by room returns date ranges | Automated |
| API-025 | Booking | Update booking | P2 | Yes | `features/api/bookings.feature` | API-025 Update booking changes dates | Automated |
| API-026 | Booking | Delete booking | P2 | Yes | `features/api/bookings.feature` | API-026 Delete booking then GET returns 404 | Automated |
| API-027 | Booking | Get booking without token | P2 | Yes | `features/api/bookings.feature` | API-027 Get booking without token returns 401 | Automated |
| API-028 | Message | Send contact message | P1 | Yes | `features/api/messages.feature` | API-028 Send contact message returns success | Automated |
| API-029 | Message | Send invalid message | P2 | Yes | `features/api/messages.feature` | API-029 Send message with short description returns 400 | Automated |
| API-030 | Message | List messages (admin) | P2 | Yes | `features/api/messages.feature` | API-030 List messages as admin returns the sent message | Automated |
| API-031 | Message | Get message by id | P2 | Yes | `features/api/messages.feature` | API-031 Get message by id returns correct fields | Automated |
| API-032 | Message | Mark message as read | P3 | Yes | `features/api/messages.feature` | API-032 Mark message as read sets read flag | Automated |
| API-033 | Message | Delete message | P3 | Yes | `features/api/messages.feature` | API-033 Delete message then GET returns 404 | Automated |
| API-034 | Report | Get report (admin) | P3 | Yes | `features/api/report.feature` | API-034 Get report as admin returns 200 | Automated |
| API-035 | Report | Get report without token | P3 | Yes | `features/api/report.feature` | API-035 Get report without token returns 401 | Automated |
| API-036 | Branding | Get branding | P3 | Yes | `features/api/branding.feature` | API-036 Get branding returns 200 with name and contact | Automated |
| API-037 | Branding | Update branding (admin) | P3 | Yes | `features/api/branding.feature` | API-037 Update branding name as admin then restore | Automated |
| API-038 | General | Unsupported HTTP method | P3 | Yes | `features/api/branding.feature` | API-038 Unsupported method on room list returns 405 | Automated |
| API-039 | General | Response headers and time | P3 | Yes | `features/api/branding.feature` | API-039 Room list responds within 2 seconds with JSON content-type | Automated (NFR soft assertion) |
| E2E-001 | Room | Room created via API shows on UI | P1 | Yes | `features/e2e/cross_layer.feature` | E2E-001 Room created via API shows on UI home page | Automated |
| E2E-002 | Booking | Booking made on UI is stored in API | P1 | Yes | `features/e2e/cross_layer.feature` | E2E-002 Booking made on UI is stored in API | Automated |
| E2E-003 | Booking | Booking created via API shows in admin UI | P1 | Yes | `features/e2e/cross_layer.feature` | E2E-003 Booking created via API shows in admin calendar | Automated |
| E2E-004 | Booking | API-booked dates conflict in UI | P2 | Yes | `features/e2e/cross_layer.feature` | E2E-004 API-booked dates conflict in UI | Automated |
| E2E-005 | Message | Contact message from UI visible via API | P2 | Yes | `features/e2e/cross_layer.feature` | E2E-005 Contact message from UI visible via API | Automated |
| E2E-006 | Room | Room deleted in admin UI returns 404 on API | P2 | Yes | `features/e2e/cross_layer.feature` | E2E-006 Room deleted in admin UI returns 404 on API | Automated |
| E2E-007 | Room | Price update via API reflected on UI | P2 | Yes | `features/e2e/cross_layer.feature` | E2E-007 Price update via API reflected on UI | Automated |
| E2E-008 | Lifecycle | Full lifecycle with cleanup | P1 | Yes | `features/e2e/cross_layer.feature` | E2E-008 Full lifecycle with cleanup | Automated |
| E2E-009 | Branding | Branding update via API reflected on UI | P3 | Yes | `features/e2e/cross_layer.feature` | E2E-009 Branding update via API reflected on UI then restored | Automated |
| E2E-010 | Auth | UI logout invalidates API token | P3 | Yes | `features/e2e/cross_layer.feature` | E2E-010 UI logout invalidates the API token | Automated (xfail - session cookie decoupling) |