from datetime import datetime, timedelta

import pytest

from prcop.business_hours import business_hours_between_dates, within_business_hours


def parse(s):
    return datetime.strptime(s, "%a, %d %b %Y %H:%M:%S")


@pytest.mark.parametrize(
    "date, business_hours",
    [
        ("Mon, 4 Feb 2019 08:59:59", False),
        ("Mon, 4 Feb 2019 09:00:00", True),
        ("Mon, 4 Feb 2019 17:00:00", True),
        ("Mon, 4 Feb 2019 17:00:01", False),
        ("Sat, 2 Feb 2019 09:00:00", False),
        ("Sun, 3 Feb 2019 09:00:00", False),
    ],
)
def test_within_business_hours(date, business_hours):
    dt = parse(date)
    assert within_business_hours(dt) is business_hours


def test_business_hours_between_dates_for_dates_within_day_and_business_hours():
    start = parse("Mon, 4 Feb 2019 09:00:00")
    end = parse("Mon, 4 Feb 2019 17:00:00")
    assert business_hours_between_dates(start, end) == timedelta(hours=8)


def test_business_hours_between_dates_within_day_and_outside_business_hours():
    start = parse("Mon, 4 Feb 2019 00:00:00")
    end = parse("Mon, 4 Feb 2019 23:59:59")
    assert business_hours_between_dates(start, end) == timedelta(hours=8)


def test_business_hours_between_dates_across_weekdays():
    start = parse("Mon, 4 Feb 2019 00:00:00")
    end = parse("Tue, 5 Feb 2019 23:59:59")
    assert business_hours_between_dates(start, end) == timedelta(hours=16)


def test_business_hours_between_dates_across_weekdays_before_start_of_business_hours():
    start = parse("Mon, 4 Feb 2019 00:00:00")
    end = parse("Tue, 5 Feb 2019 08:59:59")
    assert business_hours_between_dates(start, end) == timedelta(hours=8)


def test_business_hours_between_dates_across_weekdays_after_end_of_business_hours():
    start = parse("Mon, 4 Feb 2019 18:00:00")
    end = parse("Tue, 5 Feb 2019 10:00:00")
    assert business_hours_between_dates(start, end) == timedelta(hours=1)


def test_business_hours_between_dates_across_weekend():
    start = parse("Fri, 1 Feb 2019 00:00:00")
    end = parse("Mon, 4 Feb 2019 23:59:59")
    assert business_hours_between_dates(start, end) == timedelta(hours=16)


def test_business_hours_starting_on_weekend():
    start = parse("Sat, 2 Feb 2019 10:00:00")
    end = parse("Mon, 4 Feb 2019 10:00:00")
    assert business_hours_between_dates(start, end) == timedelta(hours=1)


def test_business_hours_ending_on_weekend():
    start = parse("Fri, 1 Feb 2019 10:00:00")
    end = parse("Sun, 3 Feb 2019 10:00:00")
    assert business_hours_between_dates(start, end) == timedelta(hours=7)


def test_business_hours_starting_and_ending_on_weekend():
    start = parse("Sat, 2 Feb 2019 10:00:00")
    end = parse("Sun, 3 Feb 2019 13:00:00")
    assert business_hours_between_dates(start, end) == timedelta(hours=0)


def test_business_hours_over_weeks():
    start = parse("Mon, 4 Feb 2019 10:00:00")
    end = parse("Mon, 18 Feb 2019 10:00:00")
    assert business_hours_between_dates(start, end) == timedelta(hours=80)


def test_business_hours_with_microseconds():
    start = datetime(2019, 2, 4, 9, 1, 2, 3)
    end = datetime(2019, 2, 5, 9, 1, 2, 4)
    assert business_hours_between_dates(start, end) == timedelta(hours=8, microseconds=1)
