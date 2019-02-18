from datetime import datetime, timedelta

from behave import given, then, when

import prcop


@given('a PR named "{name}" is opened on {time}')
def step_impl(context, name, time):
    context.name = name
    context.reviewers = []
    dt = _parse_time_str(time)
    context.frozen_datetime.move_to(dt)
    context.opened = dt.timestamp() * 1000


@given("the repo has {count:d} approvals")  # noqa: F811
def step_impl(context, count):
    context.reviewers += [{"status": "APPROVED"}] * count


@given("the repo has {count:d} needs-works")  # noqa: F811
def step_impl(context, count):
    context.reviewers += [{"status": "NEEDS_WORK"}] * count


@given("we check if reviews are due")  # noqa: F811
def step_impl(context):
    _check(context)


@given("we wait {value:d} {unit}")  # noqa: F811
def step_impl(context, value, unit):
    if not unit.endswith("s"):
        unit += "s"
    context.frozen_datetime.tick(delta=timedelta(**{unit: value}))


@given("the time is {time}")  # noqa: F811
def step_impl(context, time):
    context.frozen_datetime.move_to(_parse_time_str(time))


@when("we check if reviews are due")  # noqa: F811
def step_impl(context):
    context.alerts = _check(context)


@then("check will return {num_alerts:d} alerts")  # noqa: F811
def step_impl(context, num_alerts):
    assert (
        len(context.alerts) == num_alerts
    ), f"expected {num_alerts} alerts, got {len(context.alerts)}"


@then("the text of the first alert will be")  # noqa: F811
def step_impl(context):
    assert context.alerts[0] == context.text


def _check(context):
    BASE_URL = "http://bitbucket.test"
    url = f"{BASE_URL}/rest/api/1.0/projects/project1/repos/repo1/pull-requests"
    data = {
        "values": [
            {
                "id": 1,
                "title": context.name,
                "createdDate": context.opened,
                "reviewers": context.reviewers,
            }
        ]
    }
    context.requests_mock.get(url, json=data)
    return prcop.check(BASE_URL, ["project1/repo1"])


def _parse_time_str(s):
    """
    s should be: {weekday}, {day_of_month} {month} {year} at {hour}:{minute}
    """
    day, s = s.split(", ", 1)
    dt = datetime.strptime(s, "%d %b %Y at %H:%M")
    if dt.strftime("%A") != day:
        raise Exception(f"{s} is not a {day}")
    return dt
