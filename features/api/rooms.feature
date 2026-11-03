# features/api/rooms.feature
@api
Feature: Room API
  CRUD operations for /api/room.

  Background:
    Given the API is available
    And I have a valid admin token

  @smoke
  Scenario: API-008 List rooms returns 200 with rooms array
    When I GET "/api/room"
    Then the response status is 200
    And the response body is a rooms list
    And each room has required fields

  Scenario: API-009 Get room by id returns the room
    Given a room exists via API
    When I GET that room by id
    Then the response status is 200
    And the room data matches what was created

  @negative
  Scenario: API-010 Get non-existent room returns 404
    When I GET "/api/room/999999"
    Then the response status is 404

  @smoke
  Scenario: API-011 Create room with valid token returns 200
    When I create a room via API with valid data
    Then the response status is 200
    And the created room has a valid id
    And the room is retrievable by id

  @security @negative
  Scenario: API-012 Create room without token is rejected
    When I create a room via API without a token
    Then the response status is 401

  @negative
  Scenario: API-013 Create room with missing name returns 400
    When I create a room via API with missing name
    Then the response status is 400

  Scenario: API-014 Update room changes the price
    Given a room exists via API
    When I update the room price to 299 via API
    Then the response status is 200
    And GET that room shows price 299

  Scenario: API-015 Delete room then GET returns 404
    Given a room exists via API
    When I delete that room via API
    Then the delete response status is 200
    And GET that deleted room returns 404

  @contract
  Scenario: API-016 Room response matches JSON schema
    When I GET "/api/room"
    Then the response status is 200
    And each room matches the room JSON schema
