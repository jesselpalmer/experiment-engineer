"""Pipeline management for multi-step execution."""

from typing import Any

from src.core.exceptions import WorkflowError
from src.core.logging import get_logger
from src.workflows.workflow import Workflow

logger = get_logger(__name__)


class Pipeline(Workflow):
    """Extended workflow with pipeline-specific features."""

    def __init__(self, name: str):
        """Initialize the pipeline.

        Args:
            name: Name of the pipeline
        """
        super().__init__(name)
        self.parallel_steps: list[list[str]] = []

    def add_parallel_steps(self, step_names: list[str]) -> "Pipeline":
        """Add steps that can be executed in parallel.

        Args:
            step_names: Names of steps to execute in parallel

        Returns:
            Self for method chaining
        """
        self.parallel_steps.append(step_names)
        return self

    def _get_execution_order(self) -> list:
        """Get steps in execution order, respecting parallel execution."""
        # For now, use parent implementation
        # Can be extended to support true parallel execution
        return super()._get_execution_order()

