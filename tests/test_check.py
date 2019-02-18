from types import SimpleNamespace
from unittest.mock import call

from prcop.checker import check


def test_checker_returns_alerts_from_each_repo(mocker):
    MockChecker = mocker.patch("prcop.checker.Checker", autospec=True)
    mock_checker = MockChecker.return_value
    mock_checker.check.side_effect = [["alert1", "alert2"], ["alert3"]]
    alerts = check("http://test", ["project1/repo1", "project2/repo2"])
    assert alerts == ["alert1", "alert2", "alert3"]
    assert mock_checker.check.call_args_list == [
        call("project1", "repo1"),
        call("project2", "repo2"),
    ]


def test_checker_can_configure_http_client(mocker):
    config = SimpleNamespace(verify_https=False)
    MockHttpClient = mocker.patch("prcop.checker.HttpClient", autospec=True)
    check("http://test", [], config=config)
    assert MockHttpClient.call_args == call(verify_https=False)
