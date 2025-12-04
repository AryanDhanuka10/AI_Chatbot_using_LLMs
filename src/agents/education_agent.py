"""Education Agent"""

from __future__ import annotations

from src.agents.base_agent import BaseAgent
from src.agents.prompts.education_prompt import EducationPrompt


class EducationAgent(BaseAgent):
    """Agent for education & explanation tasks."""

    def __init__(self) -> None:
        super().__init__(prompt_template=EducationPrompt())
