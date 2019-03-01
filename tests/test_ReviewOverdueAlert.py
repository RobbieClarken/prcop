from dataclasses import dataclass
from datetime import timedelta

import pytest

from prcop.alerts import ReviewOverdueAlert


@dataclass
class PullRequestStub:
    title: str = "title1"
    business_hours_since_updated: timedelta = timedelta(hours=1)
    reviews_remaining: int = 1
    url: str = "http://test/pr1/"


@pytest.mark.parametrize(
    "reviews_remaining, expected_text", [(1, "needs 1 more review:"), (2, "needs 2 more reviews:")]
)
def test_ReviewOverdueAlert_formats_reviews_correctly(reviews_remaining, expected_text):
    pr = PullRequestStub(reviews_remaining=reviews_remaining)
    assert expected_text in str(ReviewOverdueAlert(pr))
