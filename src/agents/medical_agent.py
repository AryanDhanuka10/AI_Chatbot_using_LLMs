"""Medical Agent"""

from __future__ import annotations

from src.agents.base_agent import BaseAgent
from src.agents.prompts.medical_prompt import MedicalPrompt


class MedicalAgent(BaseAgent):
    """Agent for safe, non-prescriptive medical explanations."""

    def __init__(self) -> None:
        super().__init__(prompt_template=MedicalPrompt())
