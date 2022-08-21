Feature: Create user
  Creation user through api/v1/user/new endpoint

  Scenario: Positive scenario creation user test
    Given User with valid data
    When Send request to api/v1/user/new endpoint
    Then User successfully created