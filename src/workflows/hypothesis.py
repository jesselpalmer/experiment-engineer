"""Hypothesis refinement workflow."""

from src.core.registry import get_registry
from src.workflows.workflow import Workflow


class HypothesisRefinementWorkflow(Workflow):
    """Workflow for the complete hypothesis refinement process."""

    def __init__(self):
        """Initialize the hypothesis refinement workflow."""
        super().__init__("hypothesis_refinement")

        # Register agents if not already registered
        registry = get_registry()
        from src.agents.hypothesis import (
            HypothesisAnalyzerAgent,
            HypothesisRefinerAgent,
            HypothesisReviserAgent,
        )

        if not registry.is_registered("hypothesis_refiner"):
            registry.register("hypothesis_refiner", HypothesisRefinerAgent)
        if not registry.is_registered("hypothesis_analyzer"):
            registry.register("hypothesis_analyzer", HypothesisAnalyzerAgent)
        if not registry.is_registered("hypothesis_reviser"):
            registry.register("hypothesis_reviser", HypothesisReviserAgent)

        # Define workflow steps
        self.add_step(
            name="refine",
            agent_name="hypothesis_refiner",
            inputs={"hypothesis": "$hypothesis"},
        ).add_step(
            name="analyze",
            agent_name="hypothesis_analyzer",
            inputs={"refined_hypothesis": "$refine"},
            depends_on=["refine"],
        ).add_step(
            name="revise",
            agent_name="hypothesis_reviser",
            inputs={"original": "$refine", "reflection": "$analyze"},
            depends_on=["analyze"],
        )

