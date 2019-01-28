import requests_mock
from behave import given, then, when

import prcop


@given("a repo has a PR")
def step_impl(context):
    context.reviewers = []


@given("the repo has {count:d} approvals")  # noqa: F811
def step_impl(context, count):
    context.reviewers += [{"status": "APPROVED"}] * count


@given("the repo has {count:d} needs-works")  # noqa: F811
def step_impl(context, count):
    context.reviewers += [{"status": "NEEDS_WORK"}] * count


@when("we check if reviews are due")  # noqa: F811
@requests_mock.mock()
def step_impl(context, mock_requests):
    BASE_URL = "http://bitbucket.test"
    url = f"{BASE_URL}/rest/api/1.0/projects/project1/repos/repo1/pull-requests"
    data = {"values": [{"reviewers": context.reviewers}]}
    mock_requests.get(url, json=data)
    context.alerts = prcop.check(BASE_URL, "project1", "repo1")


@then("check will return {num_alerts:d} alerts")  # noqa: F811
def step_impl(context, num_alerts):
    assert len(context.alerts) == num_alerts, f"expected {num_alerts}, got {len(context.alerts)}"


@then('the text of the first alert will be "{text}"')  # noqa: F811
def step_impl(context, text):
    assert context.alerts[0] == text
