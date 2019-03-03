from dataclasses import dataclass

from prcop.reporters import SlackReporter


@dataclass
class AlertStub:
    text: str

    def __str__(self):
        return self.text


def test_SlackReporter(requests_mock):
    requests_mock.post("http://slack.test/")
    reporter = SlackReporter(url="http://slack.test/", channel="channel1")
    reporter.report([AlertStub("text1"), AlertStub("text2")])
    assert requests_mock.call_count == 2

    first_message = requests_mock.request_history[0].json()
    second_message = requests_mock.request_history[1].json()

    assert first_message["text"] == "text1"
    assert first_message["channel"] == "channel1"
    assert first_message["username"] == "PR Cop"
    assert first_message["icon_emoji"] == ":cop:"

    assert second_message["text"] == "text2"
    assert second_message["channel"] == "channel1"
