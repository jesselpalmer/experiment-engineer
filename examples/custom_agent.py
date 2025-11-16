"""Example of creating a custom agent."""

from src.config import get_settings
from src.core.agent import BaseAgent
from src.core.registry import get_registry
from src.utils.client import call_llm
from src.core.logging import setup_logging

# Setup logging
setup_logging()


class CustomHypothesisAgent(BaseAgent):
    """Custom agent example."""

    def __init__(self, model: str | None = None, provider: str | None = None):
        """Initialize the custom agent."""
        settings = get_settings()
        super().__init__(
            name="custom_hypothesis_agent",
            model=model or settings.default_model,
            provider=provider or settings.default_provider,
        )

    def _execute(self, text: str) -> str:
        """Execute the agent's logic."""
        prompt = f"Analyze this text and provide insights: {text}"

        return call_llm(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            provider=self.provider,
            system_message="You are a helpful assistant.",
            max_tokens=200,
            temperature=0.7,
        )


def main():
    """Example of using a custom agent."""
    # Register the custom agent
    registry = get_registry()
    registry.register("custom_agent", CustomHypothesisAgent)

    # Use it
    agent = registry.get_instance("custom_agent")
    result = agent.execute("This is a test hypothesis")

    print("=== Custom Agent Result ===")
    print(result)


if __name__ == "__main__":
    main()

