"""Unit tests for the CivitaiAPIClient class and related error handling.

This module contains tests for initialization, HTTP methods, error handling, and abstract methods.
"""

from unittest.mock import MagicMock, patch

import pytest

from civitai_api import CivitaiAPIClient, CivitaiAPIError, RateLimitError


class DummyClient(CivitaiAPIClient):
    def list_models(self, *args, **kwargs):
        return []

    def get_model(self, model_id):
        return None


def test_init_sets_api_key():
    client = DummyClient(api_key="testkey")
    assert client.api_key == "testkey"
    assert client.session.headers["Authorization"] == "Bearer testkey"


def test_get_uses_base_url():
    client = DummyClient()
    with patch.object(client, "_request", return_value={"ok": True}) as mock_request:
        result = client.get("models")
        assert result == {"ok": True}
        mock_request.assert_called_once()
        assert client.BASE_URL in mock_request.call_args[0][1]


def test_post_put_delete_methods():
    client = DummyClient()
    with patch.object(client, "_request", return_value={"ok": True}) as mock_request:
        assert client.post("endpoint", {"a": 1}) == {"ok": True}
        assert client.put("endpoint", {"a": 2}) == {"ok": True}
        assert client.delete("endpoint") == {"ok": True}
        assert mock_request.call_count == 3


def test_request_handles_rate_limit():
    client = DummyClient()
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception()
    with patch.object(
        client.session, "request", side_effect=RateLimitError("Rate limit exceeded")
    ):
        with pytest.raises(RateLimitError):
            client._request("GET", "url")


def test_request_handles_http_error():
    client = DummyClient()

    from requests.exceptions import HTTPError

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        response=MagicMock(status_code=400)
    )
    with patch.object(client.session, "request", return_value=mock_response):
        with pytest.raises(CivitaiAPIError):
            client._request("GET", "url")


def test_request_handles_request_exception():
    client = DummyClient()
    from requests.exceptions import RequestException

    with patch.object(client.session, "request", side_effect=RequestException("fail")):
        with pytest.raises(CivitaiAPIError):
            client._request("GET", "url")


def test_url_encode_query():
    client = DummyClient()
    params = {"a": [1, 2], "b": "test"}
    result = client._url_encode_query(params)
    assert "a=1&a=2" in result and "b=test" in result


def test_abstract_methods():
    client = DummyClient()
    assert client.list_models() == []
    assert client.get_model(123) is None
