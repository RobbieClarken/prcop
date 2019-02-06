@fixture.requests_mock
@fixture.freezegun
Feature: we can check PRs

  Scenario: PR has no reviews
     Given a PR named "pr-name-1" is opened on Monday, 4 Feb 2019 at 09:00
       And we wait 3 hours
       And the repo has 0 approvals
      When we check if reviews are due
      Then check will return 1 alerts
       And the text of the first alert will be
           """
           project1/repo1 PR: "pr-name-1" needs reviews
           """

  Scenario: PR has a needs-work review
     Given a PR named "pr-name-1" is opened on Monday, 4 Feb 2019 at 09:00
       And the repo has 0 approvals
       And the repo has 1 needs-works
      When we check if reviews are due
      Then check will return 0 alerts

  Scenario: PR has enough approvals
     Given a PR named "pr-name-1" is opened on Monday, 4 Feb 2019 at 09:00
       And the repo has 2 approvals
      When we check if reviews are due
      Then check will return 0 alerts

  Scenario: PR has no reviews but an alert has been sent recently
     Given a PR named "pr-name-1" is opened on Monday, 4 Feb 2019 at 09:00
       And the repo has 0 approvals
       And we check if reviews are due
       And we wait 1 minute
      When we check if reviews are due
      Then check will return 0 alerts

  Scenario: An alert was sent long enough ago that another is due
     Given a PR named "pr-name-1" is opened on Monday, 4 Feb 2019 at 09:00
       And the repo has 0 approvals
       And the time is Monday, 4 Feb 2019 at 12:00
       And we check if reviews are due
       And we wait 3 hours
      When we check if reviews are due
      Then check will return 1 alerts

  Scenario: Alerts are not sent outside business hours
     Given a PR named "pr-name-1" is opened on Monday, 4 Feb 2019 at 09:00
       And the repo has 0 approvals
       And the time is Monday, 4 Feb 2019 at 17:01
      When we check if reviews are due
      Then check will return 0 alerts

  Scenario: Alerts are not sent if PR has only been opened a short time
     Given a PR named "pr-name-1" is opened on Monday, 4 Feb 2019 at 09:00
       And the time is Monday, 4 Feb 2019 at 09:01
       And the repo has 0 approvals
      When we check if reviews are due
      Then check will return 0 alerts
