"""General Agent"""

from __future__ import annotations

from src.agents.base_agent import BaseAgent
from src.agents.prompts.general_prompt import GeneralPrompt


class GeneralAgent(BaseAgent):
    """Fallback general-purpose assistant."""

    def __init__(self) -> None:
        super().__init__(prompt_template=GeneralPrompt())
