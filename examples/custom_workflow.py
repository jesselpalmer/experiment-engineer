"""Example of creating a custom workflow."""

from src.core.registry import get_registry
from src.workflows.workflow import Workflow
from src.core.logging import setup_logging

# Setup logging
setup_logging()


class CustomExperimentWorkflow(Workflow):
    """Example of a custom multi-step workflow."""

    def __init__(self):
        """Initialize the custom workflow."""
        super().__init__("custom_experiment")

        # Register agents (assuming they exist)
        registry = get_registry()
        # ... register your agents here ...

        # Define workflow steps with dependencies
        self.add_step(
            name="step1",
            agent_name="some_agent",
            inputs={"input": "$initial_input"},
        ).add_step(
            name="step2",
            agent_name="another_agent",
            inputs={"data": "$step1"},  # Uses result from step1
            depends_on=["step1"],  # Must run after step1
        ).add_step(
            name="step3",
            agent_name="final_agent",
            inputs={"data": "$step2"},
            depends_on=["step2"],
            condition="$step2",  # Only run if step2 succeeded
        )


def main():
    """Example of using a custom workflow."""
    workflow = CustomExperimentWorkflow()
    result = workflow.execute(initial_inputs={"initial_input": "some value"})

    print(f"Workflow status: {result.status.value}")
    print(f"Step results: {result.steps}")
    print(f"Final result: {result.final_result}")


if __name__ == "__main__":
    main()

