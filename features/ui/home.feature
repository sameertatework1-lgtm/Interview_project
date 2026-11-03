# features/ui/home.feature
@ui
Feature: Home Page
  Public home page sections visible on load.

  @smoke
  Scenario: UI-001 Home page loads with core sections
    Given I open the home page
    Then the branding hero is visible
    And the rooms list is visible
    And the contact form section is visible

  @regression
  Scenario: UI-002 Room cards show name type price and features
    Given I open the home page
    Then each room card shows the room type
    And each room card shows a price
    And each room card has a Book this room button

