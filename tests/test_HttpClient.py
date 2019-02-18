from prcop.config import Config
from prcop.http_client import HttpClient


def test_can_configure_HttpClient_not_to_verify_https():
    config = Config(verify_https=False)
    client = HttpClient(config)
    assert client._session.verify is False
