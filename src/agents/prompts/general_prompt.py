"""General ChatGPT-Style Prompt Template"""

from __future__ import annotations

from typing import Dict

from src.agents.prompts.base_prompt import BasePromptTemplate


class GeneralPrompt(BasePromptTemplate):
    """Prompt template for general-purpose conversation."""

    def build_prompt(self, query: str, context: Dict) -> str:
        memory = "\n".join(context.get("memory", []))

        return (
            "You are a helpful AI assistant. Be clear, concise, and friendly.\n"
            "Avoid hallucinating facts.\n\n"
            f"Conversation Memory:\n{memory}\n\n"
            f"User Query:\n{query}\n\n"
            "Answer:"
        )
