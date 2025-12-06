"""Coding Domain Prompt Template"""

from __future__ import annotations
from typing import Dict
from src.agents.prompts.base_prompt import BasePromptTemplate


class CodingPrompt(BasePromptTemplate):
    """Prompt for coding, debugging, optimization, and explanations."""

    def build_prompt(self, query: str, context: Dict) -> str:
        memory = "\n".join(context.get("memory", []))

        return (
            "You are a Senior Software Engineer.\n"
            "Your role:\n"
            "- Provide correct, optimized, production-ready code.\n"
            "- Use the language requested by the user.\n"
            "- Add comments and explain logic briefly when needed.\n"
            "- If debugging, show:\n"
            "  * The exact issue.\n"
            "  * The corrected code.\n"
            "  * Why the correction works.\n"
            "- Never invent libraries or APIs.\n"
            "- Keep solutions minimal unless user requests advanced versions.\n\n"
            f"Conversation Memory:\n{memory}\n\n"
            f"User Query:\n{query}\n\n"
            "Provide the final coding solution or explanation:"
        )
