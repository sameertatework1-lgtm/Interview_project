# features/ui/admin_rooms.feature
@ui
Feature: Admin Room Management
  Create, edit, and delete rooms in the admin panel.

  Background:
    Given I am logged in as admin

  @smoke @e2e
  Scenario: UI-022 Create room with valid data appears in list
    When I create a room via the admin UI with valid data
    Then the new room appears in the admin rooms list
    And I delete the created room for cleanup

  @negative
  Scenario: UI-023 Create room with missing name shows validation error
    When I try to create a room with no room name
    Then the room creation error is shown
    And no room is created

  @negative
  Scenario: UI-024 Create room with invalid price shows error
    When I try to create a room with price "abc"
    Then the room creation error is shown

  @regression
  Scenario: UI-025 Edit room price is saved
    Given a room exists via API for UI editing
    When I open that room in the admin panel
    And I update the room price to 175
    Then the updated price is visible

  @regression
  Scenario: UI-026 Delete room removes it from list
    Given a room exists via API for UI editing
    When I delete that room via the admin UI
    Then the room no longer appears in the admin list

  Scenario: UI-027 Room features are saved and shown
    When I create a room with features WiFi and TV via admin UI
    Then the room is created with those features
    And I delete the created room for cleanup

  @e2e
  Scenario: UI-028 Booking appears in admin calendar
    Given a room exists via API for UI editing
    And a booking exists for that room via API
    When I open that room in the admin panel
    Then the booking dates are visible in the room calendar

