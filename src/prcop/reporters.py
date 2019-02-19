from .http_client import HttpClient


class SlackReporter:
    def __init__(self, *, url, channel):
        self._url = url
        self._channel = channel
        self._http = HttpClient()

    def report(self, alerts):
        for alert in alerts:
            payload = {"channel": self._channel, "text": str(alert)}
            self._http.post(self._url, payload=payload)
