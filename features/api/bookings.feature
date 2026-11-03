# features/api/bookings.feature
@api
Feature: Booking API
  CRUD operations for /api/booking.

  Background:
    Given the API is available
    And I have a valid admin token

  @smoke
  Scenario: API-017 Create booking with valid data returns success
    Given a room exists via API
    When I create a booking for that room with valid data
    Then the response status is 201
    And the booking response contains a booking id

  @negative
  Scenario: API-018 Create booking missing lastname returns 400
    Given a room exists via API
    When I create a booking for that room missing the lastname field
    Then the response status is 400

  @negative
  Scenario: API-019 Booking with checkout before checkin is rejected
    Given a room exists via API
    When I create a booking with checkout date before checkin date
    Then the response status is 409

  @negative
  Scenario: API-020 Overlapping booking is rejected
    Given a room exists via API
    And a booking exists for that room on fixed dates
    When I create another booking for the same room on the same dates
    Then the response status is 409

  @negative
  Scenario: API-021 Booking with invalid email returns 400
    Given a room exists via API
    When I create a booking with invalid email "notanemail"
    Then the response status is 400

  Scenario: API-022 List bookings by room id returns bookings
    Given a room exists via API
    And a booking exists for that room
    When I list bookings for that room id
    Then the response status is 200
    And the booking list includes the created booking

  Scenario: API-023 Get booking by id returns correct data
    Given a room exists via API
    And a booking exists for that room
    When I get that booking by id
    Then the response status is 200
    And the booking fields match what was created

  Scenario: API-024 Booking summary by room returns date ranges
    Given a room exists via API
    And a booking exists for that room
    When I GET the booking summary for that room
    Then the response status is 200
    And the summary contains date ranges

  Scenario: API-025 Update booking changes dates
    Given a room exists via API
    And a booking exists for that room
    When I update that booking with new dates
    Then the update response status is 200
    And GET that booking shows the updated dates

  Scenario: API-026 Delete booking then GET returns 404
    Given a room exists via API
    And a booking exists for that room
    When I delete that booking via API
    Then the delete booking response status is 202
    And GET that deleted booking returns 404

  @security @negative
  Scenario: API-027 Get booking without token returns 401
    Given a room exists via API
    And a booking exists for that room
    When I get that booking by id without a token
    Then the response status is 401
