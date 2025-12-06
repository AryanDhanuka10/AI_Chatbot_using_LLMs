"""Legal Domain Prompt Template"""

from __future__ import annotations
from typing import Dict
from src.agents.prompts.base_prompt import BasePromptTemplate


class LegalPrompt(BasePromptTemplate):
    """Prompt for legal concepts, rights, and terminology."""

    def build_prompt(self, query: str, context: Dict) -> str:
        memory = "\n".join(context.get("memory", []))

        return (
            "You are a Legal Information Assistant.\n"
            "Allowed:\n"
            "- Explain legal concepts, rights, clauses, definitions.\n"
            "- Summaries of laws (not jurisdiction-specific).\n"
            "- Neutral explanations of legal processes.\n\n"
            "Not Allowed:\n"
            "- No legal advice.\n"
            "- No predictions about outcomes.\n"
            "- No instructions on what action the user should take.\n"
            "- No interpretation of laws specific to a region.\n\n"
            "If user asks for legal decisions, remind them to consult a lawyer.\n\n"
            f"Conversation Memory:\n{memory}\n\n"
            f"User Query:\n{query}\n\n"
            "Provide an educational legal explanation:"
        )
