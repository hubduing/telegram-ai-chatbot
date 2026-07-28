"""
Unified LLM client supporting multiple providers (OpenAI, OpenRouter, etc.).

Add a new provider by adding a new factory function and registering it
in the PROVIDERS dict. No changes to bot.py are needed.
"""

from __future__ import annotations

from typing import Protocol

from openai import AsyncOpenAI

from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, LLM_PROVIDER


class LLMClient(Protocol):
    """Protocol that any LLM provider client must implement."""

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """Send a chat completion request and return the response text."""
        ...


class OpenAICompatibleClient:
    """Client for any OpenAI-compatible API (OpenAI, OpenRouter, etc.)."""

    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self._model = model

    async def chat(self, messages: list[dict[str, str]]) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content or "..."


PROVIDERS: dict[str, type[OpenAICompatibleClient]] = {
    "openai": OpenAICompatibleClient,
    "openrouter": OpenAICompatibleClient,
}


def create_llm() -> OpenAICompatibleClient | None:
    """
    Factory function. Returns an LLM client based on the provider
    configured in .env, or None if no API key is set.
    """
    if not LLM_API_KEY:
        return None

    provider_cls = PROVIDERS.get(LLM_PROVIDER)
    if provider_cls is None:
        raise ValueError(
            f"Unknown LLM provider: {LLM_PROVIDER}. "
            f"Available providers: {', '.join(PROVIDERS)}"
        )

    base_url = LLM_BASE_URL
    model = LLM_MODEL

    return provider_cls(api_key=LLM_API_KEY, base_url=base_url, model=model)