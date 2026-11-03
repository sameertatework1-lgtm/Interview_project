# features/api/auth.feature
@api
Feature: Authentication API
  Tests for /api/auth — login, logout, validate, health.

  Background:
    Given the API is available

  @smoke
  Scenario: API-001 Auth health check returns UP
    When I GET "/api/auth/actuator/health"
    Then the response status is 200
    And the response body contains "UP"

  @smoke
  Scenario: API-002 Login with valid credentials returns token
    When I login via API with username "admin" and password "password"
    Then the response status is 200
    And the response contains a token

  @negative
  Scenario: API-003 Login with invalid credentials is rejected
    When I login via API with username "admin" and password "wrongpassword"
    Then the response status is 401

  @negative
  Scenario: API-004 Login with missing password field returns error
    When I POST "/api/auth/login" with body:
      """
      {"username": "admin"}
      """
    Then the response status is 401

  Scenario: API-005 Validate a valid token succeeds
    Given I have a valid admin token
    When I validate the admin token
    Then the response status is 200

  @negative
  Scenario: API-006 Validate an invalid token is rejected
    When I POST "/api/auth/validate" with body:
      """
      {"token": "garbage_invalid_token_xyz"}
      """
    Then the response status is 403

  Scenario: API-007 Logout invalidates the token
    Given I obtain a fresh token for logout test
    When I logout with that token
    Then the logout response status is 200
    When I validate that token after logout
    Then the validate response status is 403
