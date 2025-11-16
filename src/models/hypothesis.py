"""Pydantic models for hypothesis-related data."""

from pydantic import BaseModel, Field


class Hypothesis(BaseModel):
    """Represents an original hypothesis."""

    text: str = Field(..., description="The hypothesis text")
    context: dict[str, str] | None = Field(
        default=None, description="Additional context about the hypothesis"
    )


class RefinedHypothesis(BaseModel):
    """Represents a refined hypothesis."""

    text: str = Field(..., description="The refined hypothesis text")
    original: str = Field(..., description="The original hypothesis text")
    improvements: list[str] | None = Field(
        default=None, description="List of improvements made"
    )


class Analysis(BaseModel):
    """Represents analysis feedback on a hypothesis."""

    text: str = Field(..., description="The analysis text")
    hypothesis: str = Field(..., description="The hypothesis that was analyzed")
    strengths: list[str] | None = Field(
        default=None, description="List of identified strengths"
    )
    weaknesses: list[str] | None = Field(
        default=None, description="List of identified weaknesses"
    )
    suggestions: list[str] | None = Field(
        default=None, description="List of improvement suggestions"
    )


class Revision(BaseModel):
    """Represents a revised hypothesis."""

    text: str = Field(..., description="The revised hypothesis text")
    original: str = Field(..., description="The original hypothesis text")
    analysis: str = Field(..., description="The analysis that informed the revision")
    changes: list[str] | None = Field(
        default=None, description="List of changes made"
    )

