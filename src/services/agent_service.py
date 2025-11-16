"""Service layer for agent orchestration."""

from typing import Any

from src.core.registry import get_registry
from src.models.agent import AgentConfig, AgentRequest, AgentResponse


class AgentService:
    """Service for managing agent execution."""

    def __init__(self):
        """Initialize the agent service."""
        self.registry = get_registry()

    def execute_agent(
        self, request: AgentRequest
    ) -> AgentResponse:
        """Execute an agent with the given request.

        Args:
            request: Agent execution request

        Returns:
            Agent execution response
        """
        # Get agent instance
        agent_kwargs = {}
        if request.config:
            if request.config.model:
                agent_kwargs["model"] = request.config.model
            if request.config.provider:
                agent_kwargs["provider"] = request.config.provider

        agent = self.registry.get_instance(request.agent_name, **agent_kwargs)

        # Execute agent
        result = agent.execute(**request.inputs)

        return AgentResponse(
            agent_name=request.agent_name,
            result=result,
            metadata={"status": "success"},
        )

    def list_agents(self) -> list[str]:
        """List all available agents.

        Returns:
            List of agent names
        """
        return self.registry.list_agents()

