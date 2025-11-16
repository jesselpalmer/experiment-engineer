"""Application settings and configuration management."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # API Keys
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")
    anthropic_api_key: str | None = Field(default=None, description="Anthropic API key")
    mistral_api_key: str | None = Field(default=None, description="Mistral API key")

    # Default LLM Settings
    default_provider: Literal["openai", "anthropic", "mistral"] = Field(
        default="openai", description="Default LLM provider"
    )
    default_model: str = Field(
        default="gpt-4o-mini", description="Default LLM model"
    )
    default_max_tokens: int = Field(
        default=250, ge=1, le=32000, description="Default maximum tokens"
    )
    default_temperature: float = Field(
        default=0.7, ge=0.0, le=2.0, description="Default temperature"
    )

    # Logging Configuration
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )
    log_format: str = Field(
        default="json",
        description="Log format: 'json' for structured, 'text' for human-readable",
    )

    # Feature Flags
    enable_metrics: bool = Field(
        default=True, description="Enable metrics collection"
    )
    enable_tracing: bool = Field(
        default=False, description="Enable distributed tracing"
    )

    # API Configuration (for web app)
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, ge=1, le=65535, description="API port")
    api_reload: bool = Field(
        default=False, description="Enable auto-reload for development"
    )

    # Database Configuration (for future use)
    database_url: str | None = Field(
        default=None, description="Database connection URL"
    )

    def get_api_key(self, provider: str) -> str | None:
        """Get API key for a specific provider."""
        provider_lower = provider.lower()
        if provider_lower == "openai":
            return self.openai_api_key
        elif provider_lower == "anthropic":
            return self.anthropic_api_key
        elif provider_lower == "mistral":
            return self.mistral_api_key
        return None


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

