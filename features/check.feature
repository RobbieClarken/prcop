Feature: we can check PRs

  Scenario: code reviews are due
     Given a repo has a PR
       And the repo has 0 approvals
      When we check if reviews are due
      Then check will return 1 alerts
       And the text of the first alert will be "project1/repo1 needs reviews"

  Scenario: code reviews are not due
     Given a repo has a PR
       And the repo has 0 approvals
       And the repo has 1 needs-works
      When we check if reviews are due
      Then check will return 0 alerts

  Scenario: code reviews are not due
     Given a repo has a PR
       And the repo has 2 approvals
      When we check if reviews are due
      Then check will return 0 alerts
