"""Module: llm.

LLM wrapper using Groq API (LLaMA-3 model).
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class LLM:
    """Wrapper for LLaMA-3 model served by Groq API."""

    def __init__(
        self,
        model_name: str = "llama-3.1-8b-instant",
        max_tokens: int = 256,
        temperature: float = 0.7,
    ) -> None:
        """Initialize Groq API client."""
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in .env")

        self.client = Groq(api_key=api_key)

    def generate(self, prompt: str, max_tokens: int | None = None) -> str:
        """Generate a response using LLaMA-3 via Groq."""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=max_tokens or self.max_tokens,
        )

        return response.choices[0].message.content
