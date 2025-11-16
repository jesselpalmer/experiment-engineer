"""Pytest configuration and shared fixtures."""

import pytest

from src.core.logging import setup_logging


@pytest.fixture(scope="session", autouse=True)
def setup_test_logging():
    """Setup logging for tests."""
    setup_logging()


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""
    return "This is a mock LLM response for testing purposes."


@pytest.fixture
def sample_hypothesis():
    """Sample hypothesis for testing."""
    return "Users who see personalized onboarding screens are more likely to upgrade."

