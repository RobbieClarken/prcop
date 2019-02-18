from .http_client import HttpClient


class SlackReporter:
    def __init__(self, *, url, channel, http=None):
        self._url = url
        self._channel = channel
        if http is None:
            http = HttpClient()
        self._http = http

    def report(self, alerts):
        for alert in alerts:
            payload = {"channel": self._channel, "text": str(alert)}
            self._http.post(self._url, payload=payload)
