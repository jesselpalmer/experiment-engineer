"""Agent registry for dynamic agent discovery and registration."""

from typing import Any, Type

from src.core.agent import BaseAgent
from src.core.exceptions import AgentError


class AgentRegistry:
    """Registry for managing agent classes and instances."""

    def __init__(self):
        """Initialize the agent registry."""
        self._agents: dict[str, Type[BaseAgent]] = {}
        self._instances: dict[str, BaseAgent] = {}

    def register(self, name: str, agent_class: Type[BaseAgent], overwrite: bool = False):
        """Register an agent class."""
        if name in self._agents and not overwrite:
            raise AgentError(f"Agent '{name}' is already registered")
        self._agents[name] = agent_class

    def get_class(self, name: str) -> Type[BaseAgent]:
        """Get an agent class by name."""
        if name not in self._agents:
            raise AgentError(f"Agent '{name}' is not registered")
        return self._agents[name]

    def get_instance(self, name: str, **kwargs: Any) -> BaseAgent:
        """Get or create an agent instance by name."""
        if name not in self._instances:
            agent_class = self.get_class(name)
            self._instances[name] = agent_class(**kwargs)
        return self._instances[name]

    def list_agents(self) -> list[str]:
        """List all registered agent names."""
        return list(self._agents.keys())

    def is_registered(self, name: str) -> bool:
        """Check if an agent is registered."""
        return name in self._agents

    def unregister(self, name: str):
        """Unregister an agent."""
        if name in self._agents:
            del self._agents[name]
        if name in self._instances:
            del self._instances[name]


# Global registry instance
_registry: AgentRegistry | None = None


def get_registry() -> AgentRegistry:
    """Get the global agent registry instance."""
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
    return _registry

