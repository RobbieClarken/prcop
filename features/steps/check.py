from datetime import datetime, timedelta

from behave import given, then, when

import prcop


@given('a repo has a PR named "{name}"')
def step_impl(context, name):
    context.name = name
    context.reviewers = []


@given("the repo has {count:d} approvals")  # noqa: F811
def step_impl(context, count):
    context.reviewers += [{"status": "APPROVED"}] * count


@given("the repo has {count:d} needs-works")  # noqa: F811
def step_impl(context, count):
    context.reviewers += [{"status": "NEEDS_WORK"}] * count


@given("we check if reviews are due")  # noqa: F811
def step_impl(context):
    BASE_URL = "http://bitbucket.test"
    url = f"{BASE_URL}/rest/api/1.0/projects/project1/repos/repo1/pull-requests"
    data = {"values": [{"id": 1, "title": context.name, "reviewers": context.reviewers}]}
    context.requests_mock.get(url, json=data)
    prcop.check(BASE_URL, "project1", "repo1")


@given("we wait {value:d} {unit}")  # noqa: F811
def step_impl(context, value, unit):
    if not unit.endswith("s"):
        unit += "s"
    context.frozen_datetime.tick(delta=timedelta(**{unit: value}))


@given("the time is {hour:d}:{minute:d} on a {day}")  # noqa: F811
def step_impl(context, hour, minute, day):
    day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    day_index = day_names.index(day)
    dt = datetime(2018, 1, 27, hour, minute)  # a sunday
    dt += timedelta(days=day_index)
    context.frozen_datetime.move_to(dt)


@when("we check if reviews are due")  # noqa: F811
def step_impl(context):
    BASE_URL = "http://bitbucket.test"
    url = f"{BASE_URL}/rest/api/1.0/projects/project1/repos/repo1/pull-requests"
    data = {"values": [{"id": 1, "title": context.name, "reviewers": context.reviewers}]}
    context.requests_mock.get(url, json=data)
    context.alerts = prcop.check(BASE_URL, "project1", "repo1")


@then("check will return {num_alerts:d} alerts")  # noqa: F811
def step_impl(context, num_alerts):
    assert (
        len(context.alerts) == num_alerts
    ), f"expected {num_alerts} alerts, got {len(context.alerts)}"


@then("the text of the first alert will be")  # noqa: F811
def step_impl(context):
    assert context.alerts[0] == context.text
