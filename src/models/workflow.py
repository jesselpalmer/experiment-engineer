"""Pydantic models for workflow execution."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class StepStatus(str, Enum):
    """Status of a workflow step."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowStep(BaseModel):
    """Represents a single step in a workflow."""

    name: str = Field(..., description="Name of the step")
    agent_name: str = Field(..., description="Name of the agent to execute")
    inputs: dict[str, Any] = Field(
        default_factory=dict, description="Input parameters for the step"
    )
    depends_on: list[str] = Field(
        default_factory=list, description="Names of steps this step depends on"
    )
    condition: str | None = Field(
        default=None, description="Condition for executing this step"
    )


class WorkflowResult(BaseModel):
    """Result of a workflow execution."""

    workflow_name: str = Field(..., description="Name of the workflow")
    status: StepStatus = Field(..., description="Overall workflow status")
    steps: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Results of each step"
    )
    final_result: Any | None = Field(
        default=None, description="Final aggregated result"
    )
    error: str | None = Field(default=None, description="Error message if failed")

