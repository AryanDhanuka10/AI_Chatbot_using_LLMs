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
            "Your role:\n"
            "- Explain concepts clearly and step-by-step.\n"
            "- Use simple language, real-life examples, and analogies.\n"
            "- Provide bullet points, definitions, comparisons, and illustrations when useful.\n"
            "- Keep answers concise unless the user explicitly asks for a deep explanation.\n"
            "- Avoid hallucinating facts; if unsure, say so.\n\n"
            f"Conversation Memory:\n{memory}\n\n"
            f"User Query:\n{query}\n\n"
            "Provide a structured educational explanation:"
        )
