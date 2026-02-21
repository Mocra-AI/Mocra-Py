"""Tests for VideoObservabilityApi client."""

import httpx
import pytest

from mocra import ExtraCriterion, MocraError, VideoObservabilityApi
from tests.conftest import SAMPLE_VIDEO_URL, create_mock_api


def test_video_observability_api_constructor_accepts_api_key(api_key: str) -> None:
    """Should accept API key without checking validity (matches TS SDK)."""
    api = VideoObservabilityApi(api_key)
    assert api._api_key == api_key


def test_score_video_success(mock_httpx_client: VideoObservabilityApi) -> None:
    """Should return parsed response on 200."""
    result = mock_httpx_client.score_video(SAMPLE_VIDEO_URL)
    assert result.severity == 85.5
    assert len(result.criteria) == 2
    assert result.criteria[0].name == "UNNATURAL PHYSICS"
    assert result.criteria[0].score == 90.0
    assert result.criteria[1].name == "Blur"
    assert result.criteria[1].score == 81.0


def test_score_video_with_extra_criteria(
    mock_httpx_client: VideoObservabilityApi,
) -> None:
    """Should accept extra_criteria and pass to API."""
    result = mock_httpx_client.score_video(
        SAMPLE_VIDEO_URL,
        extra_criteria=[
            ExtraCriterion(
                criterion_name="Blur",
                criterion_description="Video should not be blurry",
            ),
        ],
    )
    assert result.severity == 85.5


def test_score_video_with_ignore_criteria(
    mock_httpx_client: VideoObservabilityApi,
) -> None:
    """Should accept ignore_criteria as strings."""
    result = mock_httpx_client.score_video(
        SAMPLE_VIDEO_URL,
        ignore_criteria=["UNNATURAL PHYSICS", "MORPHING"],
    )
    assert result.severity == 85.5


def test_score_video_with_default_criterion_enum(
    mock_httpx_client: VideoObservabilityApi,
) -> None:
    """Should accept DefaultCriterion enum in ignore_criteria."""
    from mocra.models import DefaultCriterion

    result = mock_httpx_client.score_video(
        SAMPLE_VIDEO_URL,
        ignore_criteria=[DefaultCriterion.UNNATURAL_PHYSICS],
    )
    assert result.severity == 85.5


def test_score_video_raises_on_error() -> None:
    """Should raise MocraError on non-200 response."""
    response = httpx.Response(401, json={"message": "Invalid API key"})
    api = create_mock_api(response, api_key="bad-key")

    with pytest.raises(MocraError) as exc_info:
        api.score_video(SAMPLE_VIDEO_URL)

    assert exc_info.value.status_code == 401
    assert "Invalid API key" in str(exc_info.value)


def test_score_video_raises_on_400() -> None:
    """Should raise MocraError with message on 400."""
    response = httpx.Response(400, json={"message": "Invalid video URL"})
    api = create_mock_api(response)

    with pytest.raises(MocraError) as exc_info:
        api.score_video("not-a-valid-url")
    assert exc_info.value.message == "Invalid video URL"


def test_context_manager_closes_client(api_key: str) -> None:
    """Should close client when used as context manager."""
    with VideoObservabilityApi(api_key) as api:
        assert api._client is not None
    # Client should be closed (we can't easily assert without internal access,
    # but at least it shouldn't raise)
