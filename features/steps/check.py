from behave import given, then, when

import prcop


@given("repo has no reviews")
def step_impl(context):
    pass


@when("we check if reviews are due")  # noqa: F811
def step_impl(context):
    context.alerts = prcop.check("project1", "repo1")


@then("check will return an alert")  # noqa: F811
def step_impl(context):
    assert len(context.alerts) == 1
    alert = context.alerts[0]
    assert alert == "project1/repo1 needs reviews"
