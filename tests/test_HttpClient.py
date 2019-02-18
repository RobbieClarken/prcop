from prcop.http_client import HttpClient


def test_can_configure_HttpClient_not_to_verify_https():
    client = HttpClient(verify_https=False)
    assert client._session.verify is False
