"""Coding Domain Prompt Template"""

from __future__ import annotations

from typing import Dict

from src.agents.prompts.base_prompt import BasePromptTemplate


class CodingPrompt(BasePromptTemplate):
    """Prompt template for coding & debugging tasks."""

    def build_prompt(self, query: str, context: Dict) -> str:
        memory = "\n".join(context.get("memory", []))

        return (
            "You are a Senior Software Engineer.\n"
            "Provide clean, optimized, correct code.\n"
            "Avoid hallucinating libraries or APIs.\n"
            "If fixing bugs, explain the exact cause and corrected version.\n\n"
            f"Conversation Memory:\n{memory}\n\n"
            f"User Query:\n{query}\n\n"
            "Final Answer:"
        )
