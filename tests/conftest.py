"""Pytest fixtures."""

import httpx
import pytest

from mocra import VideoObservabilityApi
from mocra.client import OBSERVE_PATH

SAMPLE_VIDEO_URL = "https://example.com/video.mp4"
API_BASE_URL = "https://api.mocra.io/"


def _create_mock_transport(
    observe_response: httpx.Response,
    other_response: httpx.Response | None = None,
) -> httpx.MockTransport:
    """Create a mock transport that returns observe_response for /observe POST."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == OBSERVE_PATH and request.method == "POST":
            return observe_response
        return other_response or httpx.Response(
            404, json={"message": "Not found"}
        )

    return httpx.MockTransport(handler)


def create_mock_api(
    response: httpx.Response,
    api_key: str = "test-key",
) -> VideoObservabilityApi:
    """Create VideoObservabilityApi with mocked HTTP responses."""
    transport = _create_mock_transport(response)
    client = httpx.Client(transport=transport, base_url=API_BASE_URL)
    return VideoObservabilityApi(api_key, http_client=client)


@pytest.fixture
def api_key() -> str:
    """Sample API key for tests."""
    return "test-api-key"


@pytest.fixture
def sample_response() -> dict:
    """Sample API response."""
    return {
        "severity": 85.5,
        "criteria": [
            {"name": "UNNATURAL PHYSICS", "score": 90.0},
            {"name": "Blur", "score": 81.0},
        ],
    }


@pytest.fixture
def mock_httpx_client(sample_response: dict) -> VideoObservabilityApi:
    """Create VideoObservabilityApi with mocked httpx client."""
    response = httpx.Response(200, json=sample_response)
    return create_mock_api(response)
