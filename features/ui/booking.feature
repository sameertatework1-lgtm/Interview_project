# features/ui/booking.feature
@ui
Feature: Booking Panel
  Guest booking flow on the public home page.

  Background:
    Given a room exists for booking tests

  @smoke
  Scenario: UI-003 Open booking panel shows calendar and form
    Given I open the home page
    When I click Book this room on the test room
    Then the booking calendar is visible
    And the booking form fields are visible

  @smoke @e2e
  Scenario: UI-004 Create booking with valid data shows success
    Given I open the home page
    When I click Book this room on the test room
    And I select booking dates from day 10 to day 12
    And I fill guest details with valid data
    And I click the Book button
    Then the booking success message is shown

  @negative
  Scenario: UI-005 Submit booking with all fields empty shows validation errors
    Given I open the home page
    When I click Book this room on the test room
    And I click the Book button without filling anything
    Then booking validation errors are shown

  @negative
  Scenario: UI-006 Invalid email format shows email error
    Given I open the home page
    When I click Book this room on the test room
    And I fill guest details with email "abc" and valid other fields
    And I click the Book button
    Then booking validation errors are shown

  @boundary
  Scenario: UI-007 Phone number below minimum length shows error
    Given I open the home page
    When I click Book this room on the test room
    And I fill guest details with phone "1234567890" and valid other fields
    And I click the Book button
    Then booking validation errors are shown

  Scenario: UI-009 Cancel booking form closes panel
    Given I open the home page
    When I click Book this room on the test room
    And the booking calendar is visible
    And I click Cancel on the booking panel
    Then the booking panel is closed

  @negative @e2e
  Scenario: UI-010 Overlapping dates are rejected
    Given a booking already exists for the test room on fixed dates
    Given I open the home page
    When I click Book this room on the test room
    And I select the same fixed dates that are already booked
    And I fill guest details with valid data
    And I click the Book button
    Then a conflict error is shown

