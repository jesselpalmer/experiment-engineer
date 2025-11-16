"""Basic usage example for ExperimentKit."""

from src.workflows.hypothesis import HypothesisRefinementWorkflow
from src.core.logging import setup_logging

# Setup logging
setup_logging()


def main():
    """Run a basic hypothesis refinement workflow."""
    hypothesis = "Users who see personalized onboarding screens are more likely to upgrade."

    print("=== Original Hypothesis ===")
    print(hypothesis)
    print()

    # Create and run workflow
    workflow = HypothesisRefinementWorkflow()
    result = workflow.execute(initial_inputs={"hypothesis": hypothesis})

    if result.status.value == "completed":
        print("=== Refined Hypothesis ===")
        print(result.steps["refine"]["result"])
        print()

        print("=== Analysis ===")
        print(result.steps["analyze"]["result"])
        print()

        print("=== Revised Hypothesis ===")
        print(result.steps["revise"]["result"])
    else:
        print(f"Workflow failed: {result.error}")


if __name__ == "__main__":
    main()

