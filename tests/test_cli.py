import logging
from textwrap import dedent
from unittest.mock import ANY, call

import pytest
from click.testing import CliRunner

from prcop.cli import cli


def test_run_command_executes_check(mocker):
    mock_check = mocker.patch("prcop.cli.check", autospec=True)
    MockSlackReporter = mocker.patch("prcop.cli.SlackReporter", autospec=True)
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "run",
            "--bitbucket-url",
            "http://bitbucket.test/",
            "--slack-webhook",
            "http://slack.test/",
            "--slack-channel",
            "channel1",
            "project1/repo1",
            "project2/repo2",
        ],
    )
    assert result.exit_code == 0, result.output
    assert mock_check.call_args == call(
        "http://bitbucket.test/",
        ["project1/repo1", "project2/repo2"],
        reporter=MockSlackReporter.return_value,
        config=ANY,
    )
    assert MockSlackReporter.call_args == call(url="http://slack.test/", channel="channel1")


def test_run_command_takes_input_from_file(mocker, tmpdir):
    input_file = tmpdir.join("file.txt")
    input_file.write(
        dedent(
            """\
            project1/repo1
            project2/repo2
            """
        )
    )
    mock_check = mocker.patch("prcop.cli.check", autospec=True)
    MockSlackReporter = mocker.patch("prcop.cli.SlackReporter", autospec=True)
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "run",
            "--bitbucket-url",
            "http://bitbucket.test/",
            "--slack-webhook",
            "http://slack.test/",
            "--slack-channel",
            "channel1",
            "-i",
            str(input_file),
        ],
    )
    assert result.exit_code == 0, result.output
    assert mock_check.call_args == call(
        "http://bitbucket.test/",
        ["project1/repo1", "project2/repo2"],
        reporter=MockSlackReporter.return_value,
        config=ANY,
    )
    assert MockSlackReporter.call_args == call(url="http://slack.test/", channel="channel1")


def test_run_command_passes_in_optional_parameters(mocker):
    mock_check = mocker.patch("prcop.cli.check", autospec=True)
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "run",
            "--bitbucket-url",
            "http://bitbucket.test/",
            "--slack-webhook",
            "http://slack.test/",
            "--slack-channel",
            "channel1",
            "--no-verify-https",
            "--database",
            "/data/db1.json",
            "project1/repo1",
        ],
    )
    assert result.exit_code == 0, result.output
    config = mock_check.call_args[1]["config"]
    assert config.verify_https is False
    assert config.database == "/data/db1.json"


@pytest.mark.parametrize(
    "args, expected_log_level",
    [([], logging.WARNING), (["-v"], logging.INFO), (["-vv"], logging.DEBUG)],
)
def test_run_command_configures_log_level(mocker, args, expected_log_level):
    mocker.patch("prcop.cli.check", autospec=True)
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "run",
            "--bitbucket-url",
            "http://bitbucket.test/",
            "--slack-webhook",
            "http://slack.test/",
            "--slack-channel",
            "channel1",
            "project1/repo1",
            *args,
        ],
    )
    assert result.exit_code == 0, result.output
    assert logging.getLogger().level == expected_log_level
