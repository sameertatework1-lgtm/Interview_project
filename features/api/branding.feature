# features/api/branding.feature
@api
Feature: Branding API
  Branding endpoints at /api/branding.

  Background:
    Given the API is available
    And I have a valid admin token

  Scenario: API-036 Get branding returns 200 with name and contact
    When I GET "/api/branding"
    Then the response status is 200
    And the branding response contains name and contact fields

  Scenario: API-037 Update branding name as admin then restore
    Given I store the current branding data
    When I update the branding name to a unique AUTO_ value
    Then the response status is 200
    And GET branding returns the updated name
    And I restore the original branding data

  @negative
  Scenario: API-038 Unsupported method on room list returns 405
    When I send a PATCH request to "/api/room"
    Then the response status is 405

  @nfr
  Scenario: API-039 Room list responds within 2 seconds with JSON content-type
    When I GET "/api/room"
    Then the response status is 200
    And the response time is under 2000 milliseconds
    And the Content-Type header contains "application/json"
