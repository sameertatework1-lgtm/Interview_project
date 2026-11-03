# features/ui/admin_auth.feature
@ui
Feature: Admin Authentication
  Admin login, logout, and access control.

  @smoke
  Scenario: UI-016 Admin login with valid credentials shows dashboard
    Given I navigate to the admin login page
    When I login as admin with valid credentials
    Then the admin dashboard is displayed

  @negative
  Scenario: UI-017 Login with wrong password shows error
    Given I navigate to the admin login page
    When I login with username "admin" and password "wrongpassword"
    Then the login error message is shown
    And I remain on the login page

  @negative
  Scenario: UI-018 Login with empty credentials shows error
    Given I navigate to the admin login page
    When I click login without entering credentials
    Then the login error message is shown

  @smoke
  Scenario: UI-019 Logout returns to home page
    Given I am logged in as admin
    When I click logout
    Then I am on the home or login page

  @security @negative
  Scenario: UI-020 Direct access to admin URL without login shows login form
    Given I am not logged in
    When I navigate directly to the admin URL
    Then the login form is displayed not admin data

  Scenario: UI-021 Session persists after page refresh
    Given I am logged in as admin
    When I refresh the page
    Then the admin dashboard is still displayed

