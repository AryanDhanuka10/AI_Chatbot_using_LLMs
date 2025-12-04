"""Coding Agent"""

from __future__ import annotations

from src.agents.base_agent import BaseAgent
from src.agents.prompts.coding_prompt import CodingPrompt


class CodingAgent(BaseAgent):
    """Agent for coding, debugging & software-related tasks."""

    def __init__(self) -> None:
        super().__init__(prompt_template=CodingPrompt())
