"""Unit tests for LLM client utilities."""

import pytest

from src.core.exceptions import ConfigurationError
from src.utils.client import get_llm_client


@pytest.mark.unit
class TestLLMClient:
    """Tests for LLM client functions."""

    def test_get_llm_client_unsupported_provider(self):
        """Test that unsupported provider raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported provider"):
            get_llm_client(provider="unsupported")

    def test_get_llm_client_openai_missing_key(self, monkeypatch):
        """Test that missing API key raises ConfigurationError."""
        monkeypatch.setenv("OPENAI_API_KEY", "")
        from src.config import get_settings

        # Clear cache
        get_settings.cache_clear()

        with pytest.raises(ConfigurationError, match="OPENAI_API_KEY not found"):
            get_llm_client(provider="openai")

