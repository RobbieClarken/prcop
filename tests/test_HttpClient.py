from json.decoder import JSONDecodeError

import pytest

from prcop.http_client import HttpClient


def test_can_configure_HttpClient_not_to_verify_https():
    client = HttpClient(verify_https=False)
    assert client._session.verify is False


def test_HttpClient_response(requests_mock):
    requests_mock.get("http://url.test/", json={"key1": "value1"}, status_code=200)
    client = HttpClient()
    response = client.get("http://url.test/")
    assert response.status_code == 200
    assert response.json() == {"key1": "value1"}


def test_HttpClient_response_when_response_is_not_json(requests_mock):
    requests_mock.get("http://url.test/", text="not-json", status_code=200)
    client = HttpClient()
    response = client.get("http://url.test/")
    assert response.status_code == 200
    assert response.text == "not-json"
    with pytest.raises(JSONDecodeError):
        response.json()
