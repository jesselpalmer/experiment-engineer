"""Pydantic models for agent requests and responses."""

from typing import Any

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Configuration for an agent execution."""

    model: str | None = Field(default=None, description="LLM model to use")
    provider: str | None = Field(default=None, description="LLM provider to use")
    max_tokens: int | None = Field(default=None, description="Maximum tokens")
    temperature: float | None = Field(default=None, description="Temperature")
    system_message: str | None = Field(
        default=None, description="System message for the LLM"
    )


class AgentRequest(BaseModel):
    """Request to execute an agent."""

    agent_name: str = Field(..., description="Name of the agent to execute")
    inputs: dict[str, Any] = Field(..., description="Input parameters for the agent")
    config: AgentConfig | None = Field(
        default=None, description="Agent configuration"
    )


class AgentResponse(BaseModel):
    """Response from an agent execution."""

    agent_name: str = Field(..., description="Name of the agent that executed")
    result: Any = Field(..., description="The execution result")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about the execution"
    )

