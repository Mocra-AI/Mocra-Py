"""
Data models for the Mocra Observe API.
"""

from enum import Enum

from pydantic import BaseModel, Field


class DefaultCriterion(str, Enum):
    """Built-in criteria that can be removed from analysis."""

    UNNATURAL_PHYSICS = "UNNATURAL PHYSICS"
    MORPHING = "MORPHING"
    FLICKERING = "FLICKERING"
    ARTIFACTING = "ARTIFACTING"
    TEXT_ISSUES = "TEXT ISSUES"


class ExtraCriterion(BaseModel):
    """
    Extra criterion to add to the analysis.
    Matches TypeScript ExtraCriterion: { criterionName, criterionDescription }
    """

    criterion_name: str = Field(..., alias="criterionName")
    criterion_description: str = Field(..., alias="criterionDescription")

    model_config = {"populate_by_name": True}


class ObserveRequest(BaseModel):
    """Request body for the /observe endpoint."""

    video_url: str = Field(..., alias="videoUrl")
    custom_criteria: list[ExtraCriterion] = Field(
        default_factory=list, alias="customCriteria"
    )
    remove_criteria: list[str] = Field(
        default_factory=list, alias="removeCriteria"
    )

    model_config = {"populate_by_name": True}


class CriterionScore(BaseModel):
    """Per-criterion score in the response."""

    name: str
    score: float = Field(..., ge=1, le=100)


class ObserveResponse(BaseModel):
    """
    Response from the /observe endpoint.
    Matches TypeScript ScoreMap: { severity, criteria: [{ name, score }] }
    """

    severity: float = Field(..., ge=1, le=100)
    criteria: list[CriterionScore]


class ErrorResponse(BaseModel):
    """Error response from the API."""

    message: str
