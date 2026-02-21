"""
Mocra Python SDK - Observability for video generation workflows.

API mirrors the TypeScript SDK: https://github.com/Mocra-AI/Mocra

    from mocra import VideoObservabilityApi, ExtraCriterion

    api = VideoObservabilityApi("your-api-key")
    result = api.score_video(
        "https://example.org/video.mp4",
        extra_criteria=[
            ExtraCriterion(criterion_name="Blur", criterion_description="..."),
        ],
        ignore_criteria=["UNNATURAL PHYSICS"],
    )
"""

from mocra.client import MocraError, VideoObservabilityApi
from mocra.models import (
    CriterionScore,
    DefaultCriterion,
    ExtraCriterion,
    ObserveResponse,
)

__all__ = [
    "VideoObservabilityApi",
    "MocraError",
    "ExtraCriterion",
    "DefaultCriterion",
    "ObserveResponse",
    "CriterionScore",
]

__version__ = "0.1.0"
