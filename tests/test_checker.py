from unittest.mock import create_autospec

import pytest
from freezegun import freeze_time

from prcop.checker import Checker, JsonRecord
from prcop.exceptions import FailedToGetData
from prcop.http_client import HttpClient


class PR:
    def __init__(self):
        self.data = {"id": 1, "updatedDate": 0, "title": "pr-title", "reviewers": []}

    def with_approvals(self, n):
        self.data["reviewers"] += [{"status": "APPROVED"}] * n
        return self


@pytest.mark.parametrize(
    "values, alert_count",
    [
        ([], 0),
        ([PR().with_approvals(0).data], 1),
        ([PR().with_approvals(0).data, PR().with_approvals(0).data], 2),
        ([PR().with_approvals(2).data, PR().with_approvals(0).data], 1),
    ],
)
@freeze_time("Mon, 28 Jan 2019 09:00")
def test_check_checks_each_PR(requests_mock, values, alert_count):
    data = {"values": values}
    base_url = "http://test"
    url = f"{base_url}/rest/api/1.0/projects/project1/repos/repo1/pull-requests"
    requests_mock.get(url, json=data)
    mock_record = create_autospec(JsonRecord, instance=True)
    mock_record.alerted_recently.return_value = False
    checker = Checker(url=base_url, record=mock_record, http=HttpClient())
    alerts = checker.check("project1", "repo1")
    assert len(alerts) == alert_count


@freeze_time("Mon, 28 Jan 2019 09:00")
def test_check_handles_non_json(requests_mock):
    base_url = "http://test"
    url = f"{base_url}/rest/api/1.0/projects/project1/repos/repo1/pull-requests"
    requests_mock.get(url, text="not-json")
    mock_record = create_autospec(JsonRecord, instance=True)
    mock_record.alerted_recently.return_value = False
    checker = Checker(url=base_url, record=mock_record, http=HttpClient())
    with pytest.raises(FailedToGetData):
        checker.check("project1", "repo1")


@freeze_time("Mon, 28 Jan 2019 09:00")
def test_check_handles_unexpected_json(requests_mock):
    base_url = "http://test"
    url = f"{base_url}/rest/api/1.0/projects/project1/repos/repo1/pull-requests"
    requests_mock.get(url, json={})
    mock_record = create_autospec(JsonRecord, instance=True)
    mock_record.alerted_recently.return_value = False
    checker = Checker(url=base_url, record=mock_record, http=HttpClient())
    with pytest.raises(FailedToGetData):
        checker.check("project1", "repo1")
