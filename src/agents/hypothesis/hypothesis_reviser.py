"""Hypothesis revision agent."""

from src.config import get_settings
from src.core.agent import BaseAgent
from src.models.hypothesis import Analysis, RefinedHypothesis, Revision
from src.utils.client import call_llm


class HypothesisReviserAgent(BaseAgent):
    """Agent that incorporates analyzer feedback into revised hypotheses."""

    def __init__(
        self,
        model: str | None = None,
        provider: str | None = None,
    ):
        """Initialize the hypothesis reviser agent.

        Args:
            model: LLM model to use (defaults to settings default)
            provider: LLM provider to use (defaults to settings default)
        """
        settings = get_settings()
        super().__init__(
            name="hypothesis_reviser",
            model=model or settings.default_model,
            provider=provider or settings.default_provider,
        )

    def _execute(
        self,
        original: str | RefinedHypothesis,
        reflection: str | Analysis,
    ) -> str | Revision:
        """Revise a hypothesis based on analysis feedback.

        Args:
            original: The original hypothesis (string or RefinedHypothesis)
            reflection: The analysis feedback (string or Analysis)

        Returns:
            A revised hypothesis (string or Revision model)
        """
        # Extract text from models if provided
        if isinstance(original, RefinedHypothesis):
            original_text = original.text
            original_original = original.original
        else:
            original_text = str(original)
            original_original = original_text

        if isinstance(reflection, Analysis):
            reflection_text = reflection.text
        else:
            reflection_text = str(reflection)

        prompt = f"""
        You are a Hypothesis Revision Agent.

        Original hypothesis:
        "{original_text}"

        Reflection feedback:
        "{reflection_text}"

        Task:
        Produce one revised hypothesis that integrates the reflection feedback
        while remaining specific, measurable, and testable.
        """

        revised_text = call_llm(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            provider=self.provider,
            system_message="You are a precise experiment improvement agent.",
            max_tokens=250,
            temperature=0.7,
        )

        # Return Revision if inputs were models, otherwise return string
        if isinstance(original, RefinedHypothesis) and isinstance(reflection, Analysis):
            return Revision(
                text=revised_text,
                original=original_original,
                analysis=reflection_text,
            )
        return revised_text


# Backward compatibility function
def hypothesis_reviser(
    original: str,
    reflection: str,
    model: str = "gpt-4o-mini",
    provider: str = "openai",
) -> str:
    """Revise a hypothesis based on feedback (backward compatibility function).

    Args:
        original: The original hypothesis that was refined.
        reflection: The feedback/reflection from the analyzer.
        model: The model name to use.
        provider: The LLM provider to use.

    Returns:
        A revised hypothesis.
    """
    agent = HypothesisReviserAgent(model=model, provider=provider)
    return agent.execute(original, reflection)
