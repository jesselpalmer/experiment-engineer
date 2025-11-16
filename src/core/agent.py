"""Base agent interface and abstract class."""

import time
from abc import ABC, abstractmethod
from typing import Any

from src.core.exceptions import AgentError
from src.core.logging import get_logger
from src.core.metrics import get_metrics


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(
        self,
        name: str | None = None,
        model: str | None = None,
        provider: str | None = None,
    ):
        """Initialize the agent.

        Args:
            name: Agent name (defaults to class name)
            model: LLM model to use
            provider: LLM provider to use
        """
        self.name = name or self.__class__.__name__
        self.model = model
        self.provider = provider
        self.logger = get_logger(f"agent.{self.name}")
        self.metrics = get_metrics()

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the agent with error handling and metrics.

        This is the template method that defines the execution flow.
        Subclasses should implement `_execute` for the actual logic.

        Args:
            *args: Positional arguments for the agent
            **kwargs: Keyword arguments for the agent

        Returns:
            The result of agent execution

        Raises:
            AgentError: If execution fails
        """
        self.logger.info(
            f"Executing agent {self.name}",
            extra={"agent_name": self.name, "provider": self.provider, "model": self.model},
        )

        self.metrics.increment(
            "agent.executions",
            tags={"agent": self.name, "provider": self.provider or "unknown"},
        )

        start_time = time.time()

        try:
            result = self._execute(*args, **kwargs)

            duration = time.time() - start_time
            self.metrics.record_timing(
                "agent.duration",
                duration,
                tags={"agent": self.name, "status": "success"},
            )

            self.logger.info(
                f"Agent {self.name} completed successfully",
                extra={"agent_name": self.name},
            )

            return result

        except Exception as e:
            duration = time.time() - start_time
            self.metrics.record_timing(
                "agent.duration",
                duration,
                tags={"agent": self.name, "status": "error"},
            )

            self.metrics.increment(
                "agent.errors",
                tags={"agent": self.name, "error_type": type(e).__name__},
            )

            self.logger.error(
                f"Agent {self.name} failed: {str(e)}",
                extra={"agent_name": self.name},
                exc_info=True,
            )

            raise AgentError(f"Agent {self.name} execution failed: {str(e)}") from e

    @abstractmethod
    def _execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the agent's core logic.

        Subclasses must implement this method.

        Args:
            *args: Positional arguments for the agent
            **kwargs: Keyword arguments for the agent

        Returns:
            The result of agent execution
        """
        pass

    def validate_input(self, *args: Any, **kwargs: Any) -> None:
        """Validate input before execution.

        Override this method to add custom validation.

        Args:
            *args: Positional arguments to validate
            **kwargs: Keyword arguments to validate

        Raises:
            AgentError: If validation fails
        """
        pass

    def post_process(self, result: Any) -> Any:
        """Post-process the result after execution.

        Override this method to add custom post-processing.

        Args:
            result: The execution result

        Returns:
            The post-processed result
        """
        return result

