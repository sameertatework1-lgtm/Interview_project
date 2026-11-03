# features/ui/admin_messages.feature
@ui
Feature: Admin Messages
  Admin inbox for contact form messages.

  Background:
    Given I am logged in as admin

  @e2e
  Scenario: UI-029 Contact message arrives in admin inbox
    Given a contact message was sent via contact form
    When I open the admin messages inbox
    Then the message is listed with the correct subject

  Scenario: UI-030 Open and read a message shows details
    Given a contact message was sent via contact form
    When I open the admin messages inbox
    And I click on the message
    Then the message details are displayed

  Scenario: UI-031 Delete a message removes it from list
    Given a contact message was sent via contact form
    When I open the admin messages inbox
    And I delete the message
    Then the message is no longer in the list

  Scenario: UI-032 Report page shows occupancy calendar
    When I navigate to the admin report page
    Then the report calendar is visible

  @e2e
  Scenario: UI-033 Update branding details show on home page
    Given I store the current branding name
    When I update the branding name in admin to a unique value
    Then the new branding name appears on the home page
    And I restore the original branding name

  Scenario: UI-034 Home page renders on mobile viewport without horizontal scroll
    Given I open the home page on mobile viewport 375 by 812
    Then the page has no horizontal overflow
    And the Book this room button is visible on mobile

