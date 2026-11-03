# features/api/messages.feature
@api
Feature: Message API
  Contact messages via /api/message.

  Background:
    Given the API is available
    And I have a valid admin token

  @smoke
  Scenario: API-028 Send contact message returns success
    When I send a contact message via API with valid data
    Then the response status is 200

  @negative
  Scenario: API-029 Send message with short description returns 400
    When I send a contact message with description "short"
    Then the response status is 400

  Scenario: API-030 List messages as admin returns the sent message
    Given a contact message was sent via API
    When I list all messages as admin
    Then the response status is 200
    And the message list includes the sent message

  Scenario: API-031 Get message by id returns correct fields
    Given a contact message was sent via API
    When I get that message by id
    Then the response status is 200
    And the message fields match what was sent

  Scenario: API-032 Mark message as read sets read flag
    Given a contact message was sent via API
    When I mark that message as read
    Then the mark-read response status is 200

  Scenario: API-033 Delete message then GET returns 404
    Given a contact message was sent via API
    When I delete that message via API
    Then the delete message response status is 200
    And GET that message returns 404
