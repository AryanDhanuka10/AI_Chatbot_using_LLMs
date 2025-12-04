"""Legal Agent"""

from __future__ import annotations

from src.agents.base_agent import BaseAgent
from src.agents.prompts.legal_prompt import LegalPrompt


class LegalAgent(BaseAgent):
    """Agent for legal information responses."""

    def __init__(self) -> None:
        super().__init__(prompt_template=LegalPrompt())
