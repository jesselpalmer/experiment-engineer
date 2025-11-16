"""Hypothesis refinement agent."""

from src.config import get_settings
from src.core.agent import BaseAgent
from src.models.hypothesis import Hypothesis, RefinedHypothesis
from src.utils.client import call_llm


class HypothesisRefinerAgent(BaseAgent):
    """Agent that refines hypotheses to make them more specific and testable."""

    def __init__(
        self,
        model: str | None = None,
        provider: str | None = None,
    ):
        """Initialize the hypothesis refiner agent.

        Args:
            model: LLM model to use (defaults to settings default)
            provider: LLM provider to use (defaults to settings default)
        """
        settings = get_settings()
        super().__init__(
            name="hypothesis_refiner",
            model=model or settings.default_model,
            provider=provider or settings.default_provider,
        )

    def _execute(self, hypothesis: str | Hypothesis) -> str | RefinedHypothesis:
        """Refine a hypothesis to make it more specific, measurable, and testable.

        Args:
            hypothesis: The original hypothesis (string or Hypothesis model)

        Returns:
            A refined hypothesis (string or RefinedHypothesis model)
        """
        # Extract text from Hypothesis model if provided
        if isinstance(hypothesis, Hypothesis):
            hypothesis_text = hypothesis.text
        else:
            hypothesis_text = str(hypothesis)

        prompt = f"""
        You are a Hypothesis Refinement Agent.

        Task:
        Given the following hypothesis, rewrite it to make it more specific,
        measurable, and testable. Use clear metrics or conditions where possible.

        Original hypothesis:
        "{hypothesis_text}"

        Output:
        A single refined hypothesis that is concrete, falsifiable, and written
        in one or two sentences.
        """

        refined_text = call_llm(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            provider=self.provider,
            system_message="You are a helpful experiment design assistant.",
            max_tokens=250,
            temperature=0.7,
        )

        # Return RefinedHypothesis if input was Hypothesis, otherwise return string
        if isinstance(hypothesis, Hypothesis):
            return RefinedHypothesis(
                text=refined_text,
                original=hypothesis_text,
            )
        return refined_text


# Backward compatibility function
def hypothesis_refiner(
    hypothesis: str,
    model: str = "gpt-4o-mini",
    provider: str = "openai",
) -> str:
    """Refine a hypothesis (backward compatibility function).

    Args:
        hypothesis: The original hypothesis to refine.
        model: The model name to use.
        provider: The LLM provider to use.

    Returns:
        A refined hypothesis.
    """
    agent = HypothesisRefinerAgent(model=model, provider=provider)
    return agent.execute(hypothesis)
