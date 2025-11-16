"""Service layer for workflow management."""

from src.models.workflow import WorkflowResult
from src.workflows.hypothesis import HypothesisRefinementWorkflow


class WorkflowService:
    """Service for managing workflow execution."""

    def execute_hypothesis_refinement(
        self, hypothesis: str
    ) -> WorkflowResult:
        """Execute the hypothesis refinement workflow.

        Args:
            hypothesis: The original hypothesis to refine

        Returns:
            Workflow execution result
        """
        workflow = HypothesisRefinementWorkflow()
        return workflow.execute(initial_inputs={"hypothesis": hypothesis})

