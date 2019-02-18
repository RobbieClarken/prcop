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
    assert requests_mock.request_history[0].json() == {"text": "text1", "channel": "channel1"}
    assert requests_mock.request_history[1].json() == {"text": "text2", "channel": "channel1"}
