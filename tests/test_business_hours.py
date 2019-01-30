from datetime import datetime

import pytest

from prcop.business_hours import within_business_hours


@pytest.mark.parametrize(
    "date, business_hours",
    [
        ("Mon, 28 Jan 2019 08:59:59", False),
        ("Mon, 28 Jan 2019 09:00:00", True),
        ("Mon, 28 Jan 2019 17:00:00", True),
        ("Mon, 28 Jan 2019 17:00:01", False),
        ("Sat, 26 Jan 2019 09:00:00", False),
        ("Sat, 27 Jan 2019 09:00:00", False),
    ],
)
def test_within_business_hours(date, business_hours):
    dt = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S")
    assert within_business_hours(dt) is business_hours
