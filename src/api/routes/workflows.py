"""Workflow execution API routes."""

from fastapi import APIRouter, HTTPException

from src.core.exceptions import WorkflowError
from src.workflows.hypothesis import HypothesisRefinementWorkflow

router = APIRouter()


@router.post("/hypothesis-refinement/execute")
async def execute_hypothesis_refinement(hypothesis: str) -> dict:
    """Execute the hypothesis refinement workflow.

    Args:
        hypothesis: The original hypothesis to refine

    Returns:
        Workflow execution results

    Raises:
        HTTPException: If workflow execution fails
    """
    try:
        workflow = HypothesisRefinementWorkflow()
        result = workflow.execute(initial_inputs={"hypothesis": hypothesis})

        return {
            "workflow_name": result.workflow_name,
            "status": result.status.value,
            "steps": result.steps,
            "final_result": result.final_result,
            "error": result.error,
        }

    except WorkflowError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

