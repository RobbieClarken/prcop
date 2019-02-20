import json
from dataclasses import dataclass

import requests
import urllib3


@dataclass
class HttpResponse:
    status_code: int
    text: str

    def json(self):
        return json.loads(self.text)


class HttpClient:
    def __init__(self, *, verify_https=True):
        self._session = requests.Session()
        if not verify_https:
            self._session.verify = False
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get(self, url):
        response = self._session.get(url)
        return HttpResponse(status_code=response.status_code, text=response.text)

    def post(self, url, payload={}):
        self._session.post(url, json=payload)
