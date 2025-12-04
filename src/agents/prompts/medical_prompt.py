"""Medical Domain Prompt Template"""

from __future__ import annotations

from typing import Dict

from src.agents.prompts.base_prompt import BasePromptTemplate


class MedicalPrompt(BasePromptTemplate):
    """Prompt template for medical questions with safety guardrails."""

    def build_prompt(self, query: str, context: Dict) -> str:
        memory = "\n".join(context.get("memory", []))

        return (
            "You are a Medical Information Assistant.\n"
            "Provide factual, safe, symptom-based explanations.\n"
            "Never diagnose. Never prescribe medicine.\n"
            "Always include a disclaimer like:\n"
            "'This is not medical advice. Consult a professional.'\n\n"
            f"Conversation Memory:\n{memory}\n\n"
            f"User Query:\n{query}\n\n"
            "Respond safely and informatively:"
        )
