"""Integration tests for workflows."""

import pytest

from src.workflows.hypothesis import HypothesisRefinementWorkflow


@pytest.mark.integration
@pytest.mark.slow
class TestHypothesisRefinementWorkflow:
    """Integration tests for hypothesis refinement workflow."""

    def test_workflow_initialization(self):
        """Test workflow can be initialized."""
        workflow = HypothesisRefinementWorkflow()
        assert workflow.name == "hypothesis_refinement"
        assert len(workflow.steps) == 3

    def test_workflow_steps_defined(self):
        """Test that workflow has correct steps."""
        workflow = HypothesisRefinementWorkflow()
        step_names = [step.name for step in workflow.steps]
        assert "refine" in step_names
        assert "analyze" in step_names
        assert "revise" in step_names

