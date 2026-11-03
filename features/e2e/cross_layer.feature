# features/e2e/cross_layer.feature
@e2e
Feature: Cross-Layer End-to-End Tests
  Tests that combine API setup with UI verification and vice versa.

  Background:
    Given the API is available
    And I have a valid admin token

  @smoke
  Scenario: E2E-001 Room created via API shows on UI home page
    When I create a room via API with unique data
    Then I open the home page
    And the room card for that room is visible on the home page

  @smoke
  Scenario: E2E-002 Booking made on UI is stored in API
    Given a room exists via API
    And I open the home page
    When I book that room through the UI with unique guest data
    Then I query the API for bookings of that room
    And the booking is found in the API with matching guest data

  Scenario: E2E-003 Booking created via API shows in admin calendar
    Given a room exists via API
    And a booking exists for that room via API
    When I log in to admin and open that room
    Then the booking dates are shown in the admin calendar

  @negative
  Scenario: E2E-004 API-booked dates conflict in UI
    Given a room exists via API
    And a booking exists for that room on fixed dates via API
    When I try to book the same room on the same dates via UI
    Then a conflict error is shown on the UI

  Scenario: E2E-005 Contact message from UI visible via API
    When I submit a contact message via the UI with a unique subject
    Then I query the API for messages as admin
    And the message with that subject is found in the API

  Scenario: E2E-006 Room deleted in admin UI returns 404 on API
    Given a room exists via API
    When I delete that room via the admin UI
    Then GET that room via API returns 404

  Scenario: E2E-007 Price update via API reflected on UI
    Given a room exists via API
    When I update that room price to 199 via API
    Then the home page shows price 199 for that room

  @smoke
  Scenario: E2E-008 Full lifecycle with cleanup
    Given I obtain a fresh admin token for lifecycle test
    When I create a room via API with lifecycle test data
    And I book that room through the UI with lifecycle guest data
    Then the booking exists in the API
    And the booking appears in the admin calendar
    And I delete the booking via API
    And I delete the room via API
    And the room is no longer on the home page

  Scenario: E2E-009 Branding update via API reflected on UI then restored
    Given I store the current branding via API
    When I update the branding name via API to a unique value
    Then the home page shows the updated branding name
    And I restore the original branding via API

  @security
  Scenario: E2E-010 UI logout invalidates the API token
    Given I log in via admin UI and capture the token
    When I click logout in the admin UI
    Then the captured token is no longer valid via API

