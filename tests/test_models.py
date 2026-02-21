"""Tests for mocra models."""

import pytest
from pydantic import ValidationError

from mocra.models import (
    CriterionScore,
    DefaultCriterion,
    ExtraCriterion,
    ObserveResponse,
)


def test_extra_criterion_serialization() -> None:
    """ExtraCriterion should serialize with camelCase aliases."""
    c = ExtraCriterion(
        criterion_name="Blur",
        criterion_description="No blur allowed",
    )
    d = c.model_dump(by_alias=True)
    assert d["criterionName"] == "Blur"
    assert d["criterionDescription"] == "No blur allowed"


def test_default_criterion_values() -> None:
    """DefaultCriterion should have correct string values."""
    assert DefaultCriterion.UNNATURAL_PHYSICS.value == "UNNATURAL PHYSICS"
    assert DefaultCriterion.TEXT_ISSUES.value == "TEXT ISSUES"


def test_observe_response_validation() -> None:
    """ObserveResponse should validate severity and criteria."""
    r = ObserveResponse(severity=75.5, criteria=[CriterionScore(name="A", score=80)])
    assert r.severity == 75.5
    assert r.criteria[0].name == "A"
    assert r.criteria[0].score == 80


def test_observe_response_rejects_invalid_severity() -> None:
    """ObserveResponse should reject severity outside 1-100."""
    with pytest.raises(ValidationError):
        ObserveResponse(severity=0, criteria=[])
    with pytest.raises(ValidationError):
        ObserveResponse(severity=101, criteria=[])
