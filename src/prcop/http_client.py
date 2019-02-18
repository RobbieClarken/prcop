import requests
import urllib3


class HttpClient:
    def __init__(self, *, verify_https=True):
        self._session = requests.Session()
        if not verify_https:
            self._session.verify = False
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get(self, url):
        return self._session.get(url).json()

    def post(self, url, payload={}):
        self._session.post(url, json=payload)
