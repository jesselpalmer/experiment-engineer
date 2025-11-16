"""Unit tests for agents."""

import pytest

from src.agents.hypothesis import (
    HypothesisAnalyzerAgent,
    HypothesisRefinerAgent,
    HypothesisReviserAgent,
)


@pytest.mark.unit
class TestHypothesisRefinerAgent:
    """Tests for HypothesisRefinerAgent."""

    def test_agent_initialization(self):
        """Test agent can be initialized."""
        agent = HypothesisRefinerAgent()
        assert agent.name == "hypothesis_refiner"
        assert agent.model is not None
        assert agent.provider is not None

    def test_agent_initialization_with_params(self):
        """Test agent initialization with custom parameters."""
        agent = HypothesisRefinerAgent(model="gpt-4", provider="openai")
        assert agent.model == "gpt-4"
        assert agent.provider == "openai"


@pytest.mark.unit
class TestHypothesisAnalyzerAgent:
    """Tests for HypothesisAnalyzerAgent."""

    def test_agent_initialization(self):
        """Test agent can be initialized."""
        agent = HypothesisAnalyzerAgent()
        assert agent.name == "hypothesis_analyzer"


@pytest.mark.unit
class TestHypothesisReviserAgent:
    """Tests for HypothesisReviserAgent."""

    def test_agent_initialization(self):
        """Test agent can be initialized."""
        agent = HypothesisReviserAgent()
        assert agent.name == "hypothesis_reviser"

