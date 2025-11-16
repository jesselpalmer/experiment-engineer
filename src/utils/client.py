"""LLM client initialization utilities for multiple providers."""

import time
from typing import Protocol, Union

from src.config import get_settings
from src.core.exceptions import ConfigurationError, LLMError
from src.core.logging import get_logger
from src.core.metrics import get_metrics

logger = get_logger(__name__)
metrics = get_metrics()

# Type definitions for LLM clients
try:
    from openai import OpenAI as OpenAIClient
except ImportError:
    OpenAIClient = None

try:
    from anthropic import Anthropic as AnthropicClient
except ImportError:
    AnthropicClient = None

try:
    from mistralai import Mistral as MistralClient
except ImportError:
    MistralClient = None

LLMClient = Union[OpenAIClient, AnthropicClient, MistralClient]

# Lazy imports to avoid requiring all providers to be installed
_openai_client: OpenAIClient | None = None
_anthropic_client: AnthropicClient | None = None
_mistral_client: MistralClient | None = None


def get_llm_client(provider: str = "openai") -> LLMClient:
    """Initialize and return an LLM client for the specified provider.

    Loads configuration from settings and creates a client for the
    specified provider using the appropriate API key.

    Args:
        provider: The LLM provider to use. Supported providers:
            - "openai" (requires OPENAI_API_KEY)
            - "anthropic" (requires ANTHROPIC_API_KEY)
            - "mistral" (requires MISTRAL_API_KEY)

    Returns:
        An initialized client instance for the specified provider.

    Raises:
        ConfigurationError: If the required API key is not found.
        ValueError: If an unsupported provider is specified.
    """
    settings = get_settings()
    provider = provider.lower()

    if provider == "openai":
        return get_openai_client()
    elif provider == "anthropic":
        return get_anthropic_client()
    elif provider == "mistral":
        return get_mistral_client()
    else:
        raise ValueError(
            f"Unsupported provider: {provider}. "
            f"Supported providers: 'openai', 'anthropic', 'mistral'"
        )


def get_openai_client() -> OpenAIClient:
    """Initialize and return an OpenAI client.

    Returns:
        OpenAI: An initialized OpenAI client instance.

    Raises:
        ConfigurationError: If OPENAI_API_KEY is not found.
    """
    global _openai_client

    if _openai_client is None:
        if OpenAIClient is None:
            raise ConfigurationError(
                "OpenAI package not installed. Install it with: pip install openai"
            )

        settings = get_settings()
        api_key = settings.get_api_key("openai")
        if not api_key:
            raise ConfigurationError("OPENAI_API_KEY not found in configuration")

        _openai_client = OpenAIClient(api_key=api_key)
        logger.info("OpenAI client initialized")

    return _openai_client


def get_anthropic_client() -> AnthropicClient:
    """Initialize and return an Anthropic client.

    Returns:
        Anthropic: An initialized Anthropic client instance.

    Raises:
        ConfigurationError: If ANTHROPIC_API_KEY is not found.
    """
    global _anthropic_client

    if _anthropic_client is None:
        if AnthropicClient is None:
            raise ConfigurationError(
                "Anthropic package not installed. Install it with: pip install anthropic"
            )

        settings = get_settings()
        api_key = settings.get_api_key("anthropic")
        if not api_key:
            raise ConfigurationError("ANTHROPIC_API_KEY not found in configuration")

        _anthropic_client = AnthropicClient(api_key=api_key)
        logger.info("Anthropic client initialized")

    return _anthropic_client


def get_mistral_client() -> MistralClient:
    """Initialize and return a Mistral client.

    Returns:
        Mistral: An initialized Mistral client instance.

    Raises:
        ConfigurationError: If MISTRAL_API_KEY is not found.
    """
    global _mistral_client

    if _mistral_client is None:
        if MistralClient is None:
            raise ConfigurationError(
                "Mistral package not installed. Install it with: pip install mistralai"
            )

        settings = get_settings()
        api_key = settings.get_api_key("mistral")
        if not api_key:
            raise ConfigurationError("MISTRAL_API_KEY not found in configuration")

        _mistral_client = MistralClient(api_key=api_key)
        logger.info("Mistral client initialized")

    return _mistral_client


def call_llm(
    messages: list[dict[str, str]],
    model: str,
    provider: str = "openai",
    system_message: str | None = None,
    max_tokens: int = 250,
    temperature: float = 0.7,
    max_retries: int = 3,
    timeout: float = 60.0,
) -> str:
    """Make a chat completion call to the specified LLM provider.

    This function abstracts away the differences between provider APIs, providing
    a unified interface for making LLM calls with retry logic and error handling.

    Args:
        messages: List of message dictionaries with "role" and "content" keys.
        model: The model name to use (e.g., "gpt-4o-mini", "claude-3-haiku").
        provider: The LLM provider to use ("openai", "anthropic", or "mistral").
        system_message: Optional system message. For Anthropic, this is passed separately.
        max_tokens: Maximum number of tokens to generate. Defaults to 250.
        temperature: Sampling temperature. Defaults to 0.7.
        max_retries: Maximum number of retry attempts. Defaults to 3.
        timeout: Request timeout in seconds. Defaults to 60.0.

    Returns:
        The generated text response from the LLM.

    Raises:
        LLMError: If the API call fails after retries.
        ConfigurationError: If the provider is not configured.
    """
    provider = provider.lower()
    settings = get_settings()

    # Use settings defaults if not provided
    if provider == settings.default_provider and model == settings.default_model:
        model = settings.default_model
        max_tokens = max_tokens or settings.default_max_tokens
        temperature = temperature if temperature != 0.7 else settings.default_temperature

    metrics.increment(
        "llm.requests",
        tags={"provider": provider, "model": model},
    )

    start_time = time.time()

    last_exception: Exception | None = None

    for attempt in range(max_retries):
        try:
            result = _call_llm_impl(
                messages=messages,
                model=model,
                provider=provider,
                system_message=system_message,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=timeout,
            )

            duration = time.time() - start_time
            metrics.record_timing(
                "llm.duration",
                duration,
                tags={"provider": provider, "model": model, "status": "success"},
            )
            metrics.increment(
                "llm.success",
                tags={"provider": provider, "model": model},
            )

            logger.info(
                f"LLM call successful",
                extra={
                    "provider": provider,
                    "model": model,
                    "duration": duration,
                    "attempt": attempt + 1,
                },
            )

            return result

        except Exception as e:
            last_exception = e
            duration = time.time() - start_time

            if attempt < max_retries - 1:
                # Exponential backoff
                wait_time = 2 ** attempt
                logger.warning(
                    f"LLM call failed (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s: {str(e)}",
                    extra={"provider": provider, "model": model, "error": str(e)},
                )
                time.sleep(wait_time)
            else:
                metrics.record_timing(
                    "llm.duration",
                    duration,
                    tags={"provider": provider, "model": model, "status": "error"},
                )
                metrics.increment(
                    "llm.errors",
                    tags={"provider": provider, "model": model, "error_type": type(e).__name__},
                )

                logger.error(
                    f"LLM call failed after {max_retries} attempts: {str(e)}",
                    extra={"provider": provider, "model": model, "error": str(e)},
                    exc_info=True,
                )

                raise LLMError(
                    f"LLM API call failed after {max_retries} attempts: {str(e)}"
                ) from e

    # Should never reach here, but just in case
    raise LLMError("LLM call failed") from last_exception


def _call_llm_impl(
    messages: list[dict[str, str]],
    model: str,
    provider: str,
    system_message: str | None,
    max_tokens: int,
    temperature: float,
    timeout: float,
) -> str:
    """Internal implementation of LLM call without retry logic."""
    client = get_llm_client(provider=provider)

    if provider == "openai":
        # Prepare messages for OpenAI
        openai_messages = []
        if system_message:
            openai_messages.append({"role": "system", "content": system_message})
        openai_messages.extend(messages)

        response = client.chat.completions.create(
            model=model,
            messages=openai_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=timeout,
        )
        return response.choices[0].message.content.strip()

    elif provider == "anthropic":
        # Anthropic uses a separate system parameter
        anthropic_messages = [msg for msg in messages if msg["role"] != "system"]

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_message or "",
            messages=anthropic_messages,
            timeout=timeout,
        )
        return response.content[0].text

    elif provider == "mistral":
        # Prepare messages for Mistral
        mistral_messages = []
        if system_message:
            mistral_messages.append({"role": "system", "content": system_message})
        mistral_messages.extend(messages)

        response = client.chat.complete(
            model=model,
            messages=mistral_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=timeout,
        )
        return response.choices[0].message.content

    else:
        raise ValueError(f"Unsupported provider: {provider}")
