"""
Module: llm

Unified wrapper supporting BOTH:
- Groq Llama 3.1 models
- OpenAI GPT (GPT-4o / GPT-3.5)

Auto-selects provider based on available API key.
"""

from __future__ import annotations
import os
import logging
from typing import Optional, Generator
from dotenv import load_dotenv
load_dotenv()


# Providers
from openai import OpenAI
import groq


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class LLM:
    """LLM wrapper that automatically picks Groq or OpenAI."""

    def __init__(
        self,
        model: str = None,
        temperature: float = 0.3,
        max_tokens: int = 512,
    ) -> None:

        self.temperature = temperature
        self.max_tokens = max_tokens

        # Provider Selection Logic
        groq_key = os.getenv("GROQ_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        if groq_key:
            # ------ GROQ MODE ------
            self.provider = "groq"
            self.client = groq.Groq(api_key=groq_key)
            self.model = model or os.getenv(
                "GROQ_MODEL",
                "llama-3.1-8b-instant"         # recommended fast model
            )
            LOGGER.info(f"Using GROQ LLM: {self.model}")

        elif openai_key:
            # ------ OPENAI MODE ------
            self.provider = "openai"
            self.client = OpenAI(api_key=openai_key)
            self.model = model or os.getenv(
                "OPENAI_MODEL",
                "gpt-4o"                       # default OpenAI model
            )
            LOGGER.info(f"Using OpenAI LLM: {self.model}")

        else:
            raise ValueError(
                "No API key found. Set either GROQ_API_KEY or OPENAI_API_KEY."
            )

    # GENERATE
    def generate(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Generate a full response from Groq or OpenAI."""
        print("====== PROMPT SENT TO LLM ======")
        print(prompt)
        print("================================")

        tokens = max_tokens or self.max_tokens

        try:
            # ------------------ GROQ ------------------
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=tokens,
                )
                msg = response.choices[0].message.content
                return msg.strip()

            # ------------------ OPENAI ------------------
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=tokens,
                )
                msg = response.choices[0].message.content
                return msg.strip()

        except Exception as err:
            LOGGER.error(f"LLM.generate() failed: {err}")
            return "ERROR: LLM generate() failed"

    # STREAM
    def stream(self, prompt: str) -> Generator[str, None, None]:
        """Streaming response from either provider."""
        try:
            # ------------------ GROQ ------------------
            if self.provider == "groq":
                stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    stream=True,
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta
                    token = delta.get("content", "")
                    if token:
                        yield token

            # ------------------ OPENAI ------------------
            else:
                stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    stream=True,
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta
                    token = delta.get("content", "")
                    if token:
                        yield token

        except Exception as err:
            LOGGER.error(f"LLM.stream() failed: {err}")
            yield "[STREAM ERROR]"
