"""Module: education_agent.

Education-focused agent using structured prompt templates.
"""

from src.agents.base_agent import BaseAgent
from src.agents.prompts.education_prompt import EducationPrompt


class EducationAgent(BaseAgent):
    """Agent specialized in handling educational queries."""

    def __init__(self) -> None:
        """Initialize an education-focused agent with its prompt template."""
        super().__init__(prompt_template=EducationPrompt())

    def run(self, query: str) -> str:
        """Generate an educational explanation."""
        prompt = self._build_prompt(query)
        response = self.llm.generate(prompt)
        self._update_memory(query, response)
        return response
