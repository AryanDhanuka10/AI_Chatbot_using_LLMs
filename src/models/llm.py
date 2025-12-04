"""Module: llm
Stable Groq wrapper.
"""

from __future__ import annotations

import logging
import os
from typing import Generator, Optional

import groq
from dotenv import load_dotenv

load_dotenv()


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class LLM:
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 512,
    ) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in environment")

        # Always load model from environment
        env_model = os.getenv("GROQ_MODEL")

        # Correct default fallback
        self.model = env_model or model or "llama-3.1-8b-instant"

        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = groq.Groq(api_key=api_key)

    def generate(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        try:
            tokens = max_tokens or self.max_tokens

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=tokens,
            )

            return response.choices[0].message.content.strip()

        except Exception as err:
            LOGGER.error(f"LLM.generate() failed: {err}")
            return f"ERROR: {err}"

    def stream(self, prompt: str) -> Generator[str, None, None]:
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True,
            )

            for chunk in stream:
                if chunk.choices:
                    token = chunk.choices[0].delta.get("content", "")
                    if token:
                        yield token

        except Exception as err:
            LOGGER.error(f"LLM.stream() failed: {err}")
            yield "[STREAM ERROR]"
