"""Base workflow system for orchestrating agent execution."""

from typing import Any

from src.core.exceptions import WorkflowError
from src.core.logging import get_logger
from src.core.metrics import get_metrics
from src.core.registry import get_registry
from src.models.workflow import StepStatus, WorkflowResult, WorkflowStep

logger = get_logger(__name__)
metrics = get_metrics()


class Workflow:
    """Base class for workflow orchestration."""

    def __init__(self, name: str):
        """Initialize the workflow.

        Args:
            name: Name of the workflow
        """
        self.name = name
        self.steps: list[WorkflowStep] = []
        self.results: dict[str, Any] = {}
        self.registry = get_registry()
        self.logger = get_logger(f"workflow.{name}")
        self.metrics = get_metrics()

    def add_step(
        self,
        name: str,
        agent_name: str,
        inputs: dict[str, Any] | None = None,
        depends_on: list[str] | None = None,
        condition: str | None = None,
    ) -> "Workflow":
        """Add a step to the workflow.

        Args:
            name: Name of the step
            agent_name: Name of the agent to execute
            inputs: Input parameters for the step
            depends_on: Names of steps this step depends on
            condition: Condition for executing this step

        Returns:
            Self for method chaining
        """
        step = WorkflowStep(
            name=name,
            agent_name=agent_name,
            inputs=inputs or {},
            depends_on=depends_on or [],
            condition=condition,
        )
        self.steps.append(step)
        return self

    def execute(self, initial_inputs: dict[str, Any] | None = None) -> WorkflowResult:
        """Execute the workflow.

        Args:
            initial_inputs: Initial input values for the workflow

        Returns:
            WorkflowResult with execution results

        Raises:
            WorkflowError: If workflow execution fails
        """
        self.logger.info(f"Starting workflow: {self.name}")
        self.metrics.increment("workflow.started", tags={"workflow": self.name})

        initial_inputs = initial_inputs or {}
        self.results = {}

        try:
            # Execute steps in order, respecting dependencies
            executed_steps = set()
            step_statuses: dict[str, StepStatus] = {}

            for step in self._get_execution_order():
                if step.name in executed_steps:
                    continue

                # Check dependencies
                if not all(dep in executed_steps for dep in step.depends_on):
                    self.logger.warning(
                        f"Step {step.name} has unmet dependencies, skipping"
                    )
                    step_statuses[step.name] = StepStatus.SKIPPED
                    continue

                # Check condition if provided
                if step.condition and not self._evaluate_condition(
                    step.condition, self.results
                ):
                    self.logger.info(f"Step {step.name} condition not met, skipping")
                    step_statuses[step.name] = StepStatus.SKIPPED
                    continue

                # Execute step
                try:
                    step_statuses[step.name] = StepStatus.RUNNING
                    result = self._execute_step(step, initial_inputs)
                    self.results[step.name] = result
                    executed_steps.add(step.name)
                    step_statuses[step.name] = StepStatus.COMPLETED

                    self.logger.info(f"Step {step.name} completed successfully")

                except Exception as e:
                    step_statuses[step.name] = StepStatus.FAILED
                    self.logger.error(
                        f"Step {step.name} failed: {str(e)}", exc_info=True
                    )
                    raise WorkflowError(f"Step {step.name} failed: {str(e)}") from e

            # Determine overall status
            if StepStatus.FAILED in step_statuses.values():
                overall_status = StepStatus.FAILED
            elif all(s == StepStatus.SKIPPED for s in step_statuses.values()):
                overall_status = StepStatus.SKIPPED
            else:
                overall_status = StepStatus.COMPLETED

            workflow_result = WorkflowResult(
                workflow_name=self.name,
                status=overall_status,
                steps={
                    name: {
                        "status": status.value,
                        "result": self.results.get(name),
                    }
                    for name, status in step_statuses.items()
                },
                final_result=self._aggregate_results(),
            )

            self.metrics.increment(
                "workflow.completed",
                tags={"workflow": self.name, "status": overall_status.value},
            )

            self.logger.info(f"Workflow {self.name} completed with status {overall_status}")
            return workflow_result

        except Exception as e:
            self.metrics.increment(
                "workflow.failed",
                tags={"workflow": self.name, "error_type": type(e).__name__},
            )
            self.logger.error(f"Workflow {self.name} failed: {str(e)}", exc_info=True)

            return WorkflowResult(
                workflow_name=self.name,
                status=StepStatus.FAILED,
                steps={},
                error=str(e),
            )

    def _get_execution_order(self) -> list[WorkflowStep]:
        """Get steps in execution order respecting dependencies."""
        # Simple topological sort
        order: list[WorkflowStep] = []
        remaining = list(self.steps)
        added = set()

        while remaining:
            progress = False
            for step in list(remaining):
                if all(dep in added for dep in step.depends_on):
                    order.append(step)
                    remaining.remove(step)
                    added.add(step.name)
                    progress = True

            if not progress:
                # Circular dependency or missing dependency
                raise WorkflowError(
                    f"Unable to resolve step dependencies: {[s.name for s in remaining]}"
                )

        return order

    def _execute_step(
        self, step: WorkflowStep, initial_inputs: dict[str, Any]
    ) -> Any:
        """Execute a single workflow step.

        Args:
            step: The step to execute
            initial_inputs: Initial input values

        Returns:
            Result of step execution
        """
        # Resolve inputs (can reference previous step results)
        resolved_inputs = self._resolve_inputs(step.inputs, initial_inputs)

        # Get agent from registry
        if not self.registry.is_registered(step.agent_name):
            raise WorkflowError(f"Agent '{step.agent_name}' is not registered")

        agent = self.registry.get_instance(step.agent_name)

        # Execute agent
        return agent.execute(**resolved_inputs)

    def _resolve_inputs(
        self,
        step_inputs: dict[str, Any],
        initial_inputs: dict[str, Any],
    ) -> dict[str, Any]:
        """Resolve step inputs, including references to previous results.

        Args:
            step_inputs: Inputs defined for the step
            initial_inputs: Initial workflow inputs

        Returns:
            Resolved inputs
        """
        resolved: dict[str, Any] = {}

        for key, value in step_inputs.items():
            if isinstance(value, str) and value.startswith("$"):
                # Reference to previous step result
                ref = value[1:]  # Remove $
                if "." in ref:
                    step_name, field = ref.split(".", 1)
                    if step_name in self.results:
                        result = self.results[step_name]
                        if isinstance(result, dict):
                            resolved[key] = result.get(field)
                        else:
                            resolved[key] = result
                    else:
                        resolved[key] = initial_inputs.get(ref, value)
                else:
                    # Reference to initial input
                    resolved[key] = initial_inputs.get(ref, value)
            else:
                resolved[key] = value

        return resolved

    def _evaluate_condition(self, condition: str, results: dict[str, Any]) -> bool:
        """Evaluate a condition for step execution.

        Args:
            condition: Condition expression
            results: Current workflow results

        Returns:
            True if condition is met
        """
        # Simple condition evaluation
        # For now, just check if a result exists
        # Can be extended with more sophisticated evaluation
        if condition.startswith("$"):
            ref = condition[1:]
            return ref in results
        return True

    def _aggregate_results(self) -> Any:
        """Aggregate results from all steps.

        Returns:
            Aggregated result
        """
        # Default: return results from last step
        if self.results and self.steps:
            last_step = self.steps[-1]
            return self.results.get(last_step.name)
        return self.results

