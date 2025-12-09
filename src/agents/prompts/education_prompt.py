"""Education Domain Prompt Template"""

from __future__ import annotations
from typing import Dict
from src.agents.prompts.base_prompt import BasePromptTemplate


class EducationPrompt(BasePromptTemplate):
    """Prompt for teaching, explaining, summarizing concepts."""

    def build_prompt(self, query: str, context: Dict) -> str:
        memory = "\n".join(context.get("memory", []))

        return (
            "You are an Education & Explanation Expert.\n"
            "Your responsibilities:\n"
            "- Explain concepts step-by-step in simple, clear language.\n"
            "- Use real-life examples, analogies, and intuitive explanations.\n"
            "- Provide definitions, comparisons, summaries, and diagrams (text-based) when useful.\n"
            "- Keep answers concise unless the user asks for deep detail.\n"
            "- Never hallucinate information; say \"I'm not sure\" when uncertain.\n\n"
            f"Conversation Memory:\n{memory}\n\n"
            f"User Query:\n{query}\n\n"
            "Provide a structured educational explanation:"
        )
