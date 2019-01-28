import pytest

import prcop


class PR:
    def __init__(self):
        self.data = {"reviewers": []}

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
def test_check_checks_each_PR(requests_mock, values, alert_count):
    data = {"values": values}
    base_url = "http://test"
    url = f"{base_url}/rest/api/1.0/projects/project1/repos/repo1/pull-requests"
    requests_mock.get(url, json=data)
    alerts = prcop.check(base_url, "project1", "repo1")
    assert len(alerts) == alert_count
