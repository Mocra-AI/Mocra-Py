"""
HTTP client for the Mocra Observe API.

API mirrors the TypeScript SDK: VideoObservabilityApi(api_key).score_video(...)
See https://github.com/Mocra-AI/Mocra
"""

import httpx

from mocra.models import (
    DefaultCriterion,
    ExtraCriterion,
    ObserveRequest,
    ObserveResponse,
)

MOCRA_API_DOMAIN = "https://api.mocra.io"
OBSERVE_PATH = "/observe"

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def _normalize_ignore_criteria(
    criteria: list[str | DefaultCriterion],
) -> list[str]:
    """Convert ignore_criteria to list of strings for API payload."""
    return [
        c.value if isinstance(c, DefaultCriterion) else str(c)
        for c in criteria
    ]


def _parse_error_message(response: httpx.Response) -> str:
    """Extract error message from failed API response."""
    try:
        body = response.json()
        return body.get("message", response.text)
    except Exception:
        return response.text


class MocraError(Exception):
    """Raised when the Mocra API returns an error."""

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"[{status_code}] {message}" if status_code else message)


class VideoObservabilityApi:
    """
    Video observability API. Matches TypeScript VideoObservabilityApi.

    Example (mirrors TS SDK):
        >>> api = VideoObservabilityApi("your-api-key")
        >>> result = api.score_video(
        ...     "http://example.org/video.mp4",
        ...     extra_criteria=[
        ...         ExtraCriterion(
        ...             criterion_name="Blur",
        ...             criterion_description="The video should not be blurry",
        ...         ),
        ...     ],
        ...     ignore_criteria=["UNNATURAL PHYSICS"],
        ... )
        >>> print(result.severity, result.criteria)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        timeout: float = 60.0,
        http_client: httpx.Client | None = None,
    ):
        """
        Initialize the API client. Matches TS: VideoObservabilityApi(apiKey).

        Args:
            api_key: Your Mocra API key.
            base_url: Override API base URL (default: https://api.mocra.io).
            timeout: Request timeout in seconds.
            http_client: Optional pre-configured httpx client.
        """
        self._api_key = api_key
        base = (base_url or MOCRA_API_DOMAIN).rstrip("/") + "/"
        self._timeout = timeout
        headers = {"Authorization": f"Bearer {api_key}", **DEFAULT_HEADERS}
        self._client = http_client or httpx.Client(
            base_url=base,
            headers=headers,
            timeout=timeout,
        )
        self._owns_client = http_client is None

    def score_video(
        self,
        video_url: str,
        extra_criteria: list[ExtraCriterion] | None = None,
        ignore_criteria: list[str | DefaultCriterion] | None = None,
    ) -> ObserveResponse:
        """
        Score a video (TS: scoreVideo(videoUrl, extraCriteria?, ignoreCriteria?)).

        Args:
            video_url: URL of the video to analyze.
            extra_criteria: Extra criteria to analyze (default: []).
            ignore_criteria: Default criteria to exclude, e.g. ["UNNATURAL PHYSICS"]
                or [DefaultCriterion.UNNATURAL_PHYSICS] (default: []).

        Returns:
            { severity, criteria: [{ name, score }] }

        Raises:
            MocraError: API returned an error.
            httpx.HTTPError: Network error.
        """
        extra = extra_criteria or []
        ignore_strs = _normalize_ignore_criteria(ignore_criteria or [])
        request = ObserveRequest(
            video_url=video_url,
            custom_criteria=extra,
            remove_criteria=ignore_strs,
        )
        return self._request(request)

    def _request(self, request: ObserveRequest) -> ObserveResponse:
        payload = request.model_dump(by_alias=True, mode="json")
        response = self._client.post(OBSERVE_PATH, json=payload)

        if response.status_code == 200:
            return ObserveResponse.model_validate(response.json())

        message = _parse_error_message(response)
        raise MocraError(message=message, status_code=response.status_code)

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "VideoObservabilityApi":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
