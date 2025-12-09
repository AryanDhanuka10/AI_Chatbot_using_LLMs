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
            "Your responsibilities:\n"
            "- Provide correct, optimized, production-ready code.\n"
            "- Use the exact programming language requested by the user.\n"
            "- Add minimal comments only when necessary.\n"
            "- If debugging, include:\n"
            "  * A clear explanation of the issue.\n"
            "  * The corrected full code.\n"
            "  * Why the fix works.\n"
            "- Never invent libraries, functions, or APIs.\n"
            "- Keep solutions minimal unless the user asks for advanced versions.\n"
            "- If the query is ambiguous, ask clarifying questions before giving code.\n\n"
            f"Conversation Memory:\n{memory}\n\n"
            f"User Query:\n{query}\n\n"
            "Provide the final coding solution or explanation:"
        )
