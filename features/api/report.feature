# features/api/report.feature
@api
Feature: Report API
  Report endpoints at /api/report.

  Background:
    Given the API is available
    And I have a valid admin token

  Scenario: API-034 Get report as admin returns 200
    When I GET "/api/report" with admin token
    Then the response status is 200
    And the report response has data

  @security @negative
  Scenario: API-035 Get report without token returns 401
    When I GET "/api/report" without a token
    Then the response status is 401
