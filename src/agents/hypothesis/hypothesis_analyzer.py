"""Hypothesis analysis agent."""

from src.config import get_settings
from src.core.agent import BaseAgent
from src.models.hypothesis import Analysis, RefinedHypothesis
from src.utils.client import call_llm


class HypothesisAnalyzerAgent(BaseAgent):
    """Agent that analyzes and provides feedback on refined hypotheses."""

    def __init__(
        self,
        model: str | None = None,
        provider: str | None = None,
    ):
        """Initialize the hypothesis analyzer agent.

        Args:
            model: LLM model to use (defaults to settings default)
            provider: LLM provider to use (defaults to settings default)
        """
        settings = get_settings()
        super().__init__(
            name="hypothesis_analyzer",
            model=model or settings.default_model,
            provider=provider or settings.default_provider,
        )

    def _execute(self, refined_hypothesis: str | RefinedHypothesis) -> str | Analysis:
        """Analyze a refined hypothesis and provide feedback.

        Args:
            refined_hypothesis: The refined hypothesis to analyze

        Returns:
            Analysis feedback (string or Analysis model)
        """
        # Extract text from RefinedHypothesis model if provided
        if isinstance(refined_hypothesis, RefinedHypothesis):
            hypothesis_text = refined_hypothesis.text
            original_text = refined_hypothesis.original
        else:
            hypothesis_text = str(refined_hypothesis)
            original_text = hypothesis_text

        prompt = f"""
        You are a Hypothesis Reflection Agent.

        Task:
        Critically evaluate the following refined hypothesis as if you are a peer reviewer
        preparing it for a real-world experiment.

        Refined hypothesis:
        "{hypothesis_text}"

        Analyze it on the following criteria:
        1. **Clarity** – Is the hypothesis clearly stated and easy to understand?
        2. **Specificity** – Does it define measurable metrics, timeframes, or success conditions?
        3. **Testability** – Could it realistically be validated or falsified with an experiment?
        4. **Assumptions** – Are there any hidden assumptions or biases?
        5. **Actionability** – Can it guide a meaningful next experiment?

        Output:
        Provide a short, structured reflection in 3–5 paragraphs that includes:
        - A summary of the hypothesis quality
        - Two concrete strengths
        - Two areas to improve
        - One actionable suggestion for refinement or next steps.
        """

        analysis_text = call_llm(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            provider=self.provider,
            system_message="You are a thoughtful and critical experiment design reviewer.",
            max_tokens=400,
            temperature=0.6,
        )

        # Return Analysis if input was RefinedHypothesis, otherwise return string
        if isinstance(refined_hypothesis, RefinedHypothesis):
            return Analysis(
                text=analysis_text,
                hypothesis=hypothesis_text,
            )
        return analysis_text


# Backward compatibility function
def hypothesis_analyzer(
    refined_hypothesis: str,
    model: str = "gpt-4o-mini",
    provider: str = "openai",
) -> str:
    """Analyze a refined hypothesis (backward compatibility function).

    Args:
        refined_hypothesis: The refined hypothesis to analyze.
        model: The model name to use.
        provider: The LLM provider to use.

    Returns:
        Analysis feedback.
    """
    agent = HypothesisAnalyzerAgent(model=model, provider=provider)
    return agent.execute(refined_hypothesis)
