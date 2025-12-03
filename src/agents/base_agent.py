"""Module: base_agent.

Defines BaseAgent class for structured LLM interaction using prompt templates
and context.
"""

from abc import ABC, abstractmethod

from src.agents.prompts.base_prompt import BasePromptTemplate
from src.models.llm import LLM
from src.utils.context_manager import ContextManager


class BaseAgent(ABC):
    """Abstract base class for all domain agents."""

    def __init__(self, prompt_template: BasePromptTemplate) -> None:
        """Initialize the base agent.

        Args:
        ----
            prompt_template: The prompt template used by the agent.

        """
        self.llm = LLM()
        self.prompt_template = prompt_template
        self.context_manager = ContextManager()

    @abstractmethod
    def run(self, query: str) -> str:
        """Generate a response using the LLM and domain-specific prompt.

        Args:
        ----
            query: User message.

        Returns:
        -------
            LLM-generated response.

        """
        raise NotImplementedError

    def _build_prompt(self, query: str) -> str:
        """Use template + context to produce final prompt string."""
        context = self.context_manager.get_context()
        return self.prompt_template.build_prompt(query, context)

    def _update_memory(self, query: str, response: str) -> None:
        """Store query + response into context memory."""
        self.context_manager.add_memory(f"User: {query}")
        self.context_manager.add_memory(f"Assistant: {response}")
