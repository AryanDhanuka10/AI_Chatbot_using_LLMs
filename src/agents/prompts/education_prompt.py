"""Education Domain Prompt Template"""

from __future__ import annotations

from typing import Dict

from src.agents.prompts.base_prompt import BasePromptTemplate


class EducationPrompt(BasePromptTemplate):
    """Prompt template for education / explanation tasks."""

    def build_prompt(self, query: str, context: Dict) -> str:
        memory = "\n".join(context.get("memory", []))

        return (
            "You are an Education Expert.\n"
            "Explain concepts clearly, step-by-step, and avoid unnecessary complexity.\n"
            "Use examples, analogies, and concise explanations.\n"
            "If code is needed, keep it simple.\n\n"
            f"Conversation Memory:\n{memory}\n\n"
            f"User Query:\n{query}\n\n"
            "Provide the final answer below:"
        )
