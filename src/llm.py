from __future__ import annotations

import asyncio
import logging
from typing import Protocol

from openai import AsyncOpenAI
from openai import APIError, APITimeoutError, RateLimitError

from src.config import settings

logger = logging.getLogger(__name__)


class LLMClient(Protocol):
    async def chat(self, messages: list[dict[str, str]]) -> str:
        ...


class OpenAICompatibleClient:
    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self._model = model
        self._max_retries = 3
        self._retry_delay = 1.0

    async def chat(self, messages: list[dict[str, str]]) -> str:
        last_exception: Exception | None = None

        for attempt in range(self._max_retries):
            try:
                response = await self._client.chat.completions.create(
                    model=self._model,
                    messages=messages,
                    max_tokens=1024,
                    temperature=0.7,
                )
                return response.choices[0].message.content or "..."

            except RateLimitError:
                wait = self._retry_delay * (2 ** attempt)
                logger.warning("Rate limited, retrying in %.1fs (attempt %d/%d)", wait, attempt + 1, self._max_retries)
                await asyncio.sleep(wait)
                last_exception = RateLimitError

            except APITimeoutError:
                wait = self._retry_delay * (2 ** attempt)
                logger.warning("API timeout, retrying in %.1fs (attempt %d/%d)", wait, attempt + 1, self._max_retries)
                await asyncio.sleep(wait)
                last_exception = APITimeoutError

            except APIError as e:
                last_exception = e
                logger.error("OpenAI API error: %s", e)
                break

        raise last_exception or RuntimeError("LLM request failed after retries")


PROVIDERS: dict[str, type[OpenAICompatibleClient]] = {
    "openai": OpenAICompatibleClient,
    "openrouter": OpenAICompatibleClient,
}


def create_llm() -> OpenAICompatibleClient | None:
    if not settings.llm_api_key:
        return None

    provider_cls = PROVIDERS.get(settings.llm_provider)
    if provider_cls is None:
        raise ValueError(
            f"Unknown LLM provider: {settings.llm_provider}. "
            f"Available providers: {', '.join(PROVIDERS)}"
        )

    return provider_cls(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        model=settings.llm_model,
    )