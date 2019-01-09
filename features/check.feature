Feature: we can check PRs

  Scenario: code reviews are due
     Given repo has no reviews
      When we check if reviews are due
      Then check will return an alert
