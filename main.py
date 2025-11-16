"""Main entry point for ExperimentKit example."""

from src.core.logging import setup_logging
from src.workflows.hypothesis import HypothesisRefinementWorkflow


def main():
    """Run the hypothesis refinement workflow example."""
    # Setup logging
    setup_logging()

    # --- Step 1: Input ---
    hypothesis = "Users who see personalized onboarding screens are more likely to upgrade."
    print("\n=== ORIGINAL HYPOTHESIS ===")
    print(hypothesis)

    # --- Step 2-4: Run workflow ---
    workflow = HypothesisRefinementWorkflow()
    result = workflow.execute(initial_inputs={"hypothesis": hypothesis})

    if result.status.value == "completed":
        print("\n=== REFINED HYPOTHESIS ===")
        print(result.steps.get("refine", {}).get("result", ""))

        print("\n=== ANALYZER FEEDBACK ===")
        print(result.steps.get("analyze", {}).get("result", ""))

        print("\n=== REVISED HYPOTHESIS ===")
        print(result.steps.get("revise", {}).get("result", ""))
    else:
        print(f"\n=== WORKFLOW FAILED ===")
        print(result.error or "Unknown error")


if __name__ == "__main__":
    main()
