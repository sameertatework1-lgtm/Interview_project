# features/ui/contact.feature
@ui
Feature: Contact Form
  Contact form submission on the home page.

  @smoke
  Scenario: UI-011 Submit valid contact form shows confirmation
    Given I open the home page
    When I fill and submit the contact form with valid data
    Then the contact success message is shown

  @negative
  Scenario: UI-012 Submit empty contact form shows validation errors
    Given I open the home page
    When I submit the contact form without filling any fields
    Then contact form validation errors are shown

  @boundary
  Scenario: UI-013 Message shorter than minimum shows length error
    Given I open the home page
    When I fill the contact form with a message of only 5 characters
    Then contact form validation errors are shown

  @negative
  Scenario: UI-014 Invalid email format in contact form shows error
    Given I open the home page
    When I fill the contact form with email "abc@"
    Then contact form validation errors are shown

  @boundary
  Scenario: UI-015 Subject too short shows length error
    Given I open the home page
    When I fill the contact form with subject "ab"
    Then contact form validation errors are shown

