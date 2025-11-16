"""Command-line interface for ExperimentKit."""

import click

from src.core.logging import setup_logging
from src.workflows.hypothesis import HypothesisRefinementWorkflow


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Set the logging level",
)
def cli(log_level: str):
    """ExperimentKit - Agentic infrastructure for experiment design."""
    # Setup logging
    from src.config import get_settings

    settings = get_settings()
    settings.log_level = log_level  # type: ignore
    setup_logging()


@cli.command()
@click.argument("hypothesis", type=str)
@click.option(
    "--model",
    type=str,
    default=None,
    help="LLM model to use (defaults to configuration)",
)
@click.option(
    "--provider",
    type=click.Choice(["openai", "anthropic", "mistral"]),
    default=None,
    help="LLM provider to use (defaults to configuration)",
)
def refine(hypothesis: str, model: str | None, provider: str | None):
    """Refine a hypothesis to make it more specific and testable."""
    from src.agents.hypothesis import hypothesis_refiner

    click.echo(f"\n=== ORIGINAL HYPOTHESIS ===")
    click.echo(hypothesis)

    refined = hypothesis_refiner(hypothesis, model=model or "gpt-4o-mini", provider=provider or "openai")

    click.echo(f"\n=== REFINED HYPOTHESIS ===")
    click.echo(refined)


@cli.command()
@click.argument("hypothesis", type=str)
@click.option(
    "--model",
    type=str,
    default=None,
    help="LLM model to use (defaults to configuration)",
)
@click.option(
    "--provider",
    type=click.Choice(["openai", "anthropic", "mistral"]),
    default=None,
    help="LLM provider to use (defaults to configuration)",
)
def analyze(hypothesis: str, model: str | None, provider: str | None):
    """Analyze a refined hypothesis and provide feedback."""
    from src.agents.hypothesis import hypothesis_analyzer

    click.echo(f"\n=== HYPOTHESIS TO ANALYZE ===")
    click.echo(hypothesis)

    analysis = hypothesis_analyzer(
        hypothesis, model=model or "gpt-4o-mini", provider=provider or "openai"
    )

    click.echo(f"\n=== ANALYSIS ===")
    click.echo(analysis)


@cli.command()
@click.argument("hypothesis", type=str)
@click.option(
    "--model",
    type=str,
    default=None,
    help="LLM model to use (defaults to configuration)",
)
@click.option(
    "--provider",
    type=click.Choice(["openai", "anthropic", "mistral"]),
    default=None,
    help="LLM provider to use (defaults to configuration)",
)
def workflow(hypothesis: str, model: str | None, provider: str | None):
    """Run the complete hypothesis refinement workflow."""
    click.echo(f"\n=== ORIGINAL HYPOTHESIS ===")
    click.echo(hypothesis)

    workflow = HypothesisRefinementWorkflow()
    result = workflow.execute(initial_inputs={"hypothesis": hypothesis})

    if result.status.value == "completed":
        click.echo(f"\n=== REFINED HYPOTHESIS ===")
        click.echo(result.steps.get("refine", {}).get("result", ""))

        click.echo(f"\n=== ANALYSIS ===")
        click.echo(result.steps.get("analyze", {}).get("result", ""))

        click.echo(f"\n=== REVISED HYPOTHESIS ===")
        click.echo(result.steps.get("revise", {}).get("result", ""))
    else:
        click.echo(f"\n=== WORKFLOW FAILED ===")
        click.echo(result.error or "Unknown error")


@cli.command()
def config():
    """Show current configuration."""
    from src.config import get_settings

    settings = get_settings()
    click.echo("=== ExperimentKit Configuration ===")
    click.echo(f"Default Provider: {settings.default_provider}")
    click.echo(f"Default Model: {settings.default_model}")
    click.echo(f"Log Level: {settings.log_level}")
    click.echo(f"Metrics Enabled: {settings.enable_metrics}")


if __name__ == "__main__":
    cli()

