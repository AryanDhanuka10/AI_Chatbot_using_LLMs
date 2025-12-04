"""Legal Domain Prompt Template"""

from __future__ import annotations

from typing import Dict

from src.agents.prompts.base_prompt import BasePromptTemplate


class LegalPrompt(BasePromptTemplate):
    """Prompt template for legal analysis & explanations."""

    def build_prompt(self, query: str, context: Dict) -> str:
        memory = "\n".join(context.get("memory", []))

        return (
            "You are a Legal Information Assistant.\n"
            "Explain legal concepts, clauses, and rights in simple language.\n"
            "Never provide legal advice or tell users what decisions to make.\n"
            "Always clarify that you are not a lawyer.\n\n"
            f"Conversation Memory:\n{memory}\n\n"
            f"User Query:\n{query}\n\n"
            "Provide an educational legal explanation:"
        )
