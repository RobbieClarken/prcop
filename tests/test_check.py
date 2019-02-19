from unittest.mock import Mock, call, create_autospec

from prcop.checker import check
from prcop.config import Config
from prcop.reporters import SlackReporter


def test_checker_reports_alerts_from_each_repo(mocker):
    MockChecker = mocker.patch("prcop.checker.Checker", autospec=True)
    mock_checker = MockChecker.return_value
    mock_checker.check.side_effect = [["alert1", "alert2"], ["alert3"]]
    mock_reporter = create_autospec(SlackReporter, instance=True)
    check("http://test", ["project1/repo1", "project2/repo2"], reporter=mock_reporter)
    alerts = mock_reporter.report.call_args[0][0]
    assert alerts == ["alert1", "alert2", "alert3"]
    assert mock_checker.check.call_args_list == [
        call("project1", "repo1"),
        call("project2", "repo2"),
    ]


def test_checker_can_configure_HttpClient(mocker):
    config = Config(verify_https=False)
    MockHttpClient = mocker.patch("prcop.checker.HttpClient", autospec=True)
    check("http://test", [], config=config, reporter=Mock())
    assert MockHttpClient.call_args == call(verify_https=False)


def test_checker_can_configure_JsonRecord(mocker):
    config = Config(database="/data/db.json")
    MockJsonRecord = mocker.patch("prcop.checker.JsonRecord", autospec=True)
    check("http://test", [], config=config, reporter=Mock())
    assert MockJsonRecord.call_args == call(database="/data/db.json")
