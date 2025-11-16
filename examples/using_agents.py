"""Example of using individual agents."""

from src.agents import hypothesis_analyzer, hypothesis_refiner, hypothesis_reviser
from src.core.logging import setup_logging

# Setup logging
setup_logging()


def main():
    """Use individual agents directly."""
    hypothesis = "Users who see personalized onboarding screens are more likely to upgrade."

    print("=== Step 1: Refine ===")
    refined = hypothesis_refiner(hypothesis)
    print(refined)
    print()

    print("=== Step 2: Analyze ===")
    analysis = hypothesis_analyzer(refined)
    print(analysis)
    print()

    print("=== Step 3: Revise ===")
    revised = hypothesis_reviser(refined, analysis)
    print(revised)


if __name__ == "__main__":
    main()

