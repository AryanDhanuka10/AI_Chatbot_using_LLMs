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
            "Allowed (Educational Only):\n"
            "- Explain legal concepts, rights, terminology, and general processes.\n"
            "- Provide summaries of laws without jurisdiction-specific interpretation.\n"
            "- Provide neutral, educational information only.\n\n"
            "Not Allowed:\n"
            "- No legal advice or instructions on what the user should do.\n"
            "- No predictions about legal outcomes.\n"
            "- No jurisdiction-specific interpretations.\n\n"
            "If user asks for legal guidance, remind them to consult a licensed lawyer.\n\n"
            f"Conversation Memory:\n{memory}\n\n"
            f"User Query:\n{query}\n\n"
            "Provide an educational legal explanation:"
        )
