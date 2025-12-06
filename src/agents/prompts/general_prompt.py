"""General Purpose Prompt Template"""

from __future__ import annotations
from typing import Dict
from src.agents.prompts.base_prompt import BasePromptTemplate


class GeneralPrompt(BasePromptTemplate):
    """Prompt for general conversation or non-domain queries."""

    def build_prompt(self, query: str, context: Dict) -> str:
        memory = "\n".join(context.get("memory", []))

        return (
            "You are a helpful and concise AI Assistant.\n"
            "- Be friendly but not overly casual.\n"
            "- Keep answers short unless user requests detail.\n"
            "- Provide bullet points or examples if helpful.\n"
            "- Never hallucinate; admit uncertainty when needed.\n"
            "- Maintain professional tone.\n\n"
            f"Conversation Memory:\n{memory}\n\n"
            f"User Query:\n{query}\n\n"
            "Provide the final answer:"
        )
