"""Module: base_prompt.

Base class for structured prompt templates used by all Agents.
"""

from abc import ABC, abstractmethod
from typing import Dict


class BasePromptTemplate(ABC):
    """Abstract base class for prompt templates.

    Child classes override build_prompt() to structure domain-specific context.
    """

    @abstractmethod
    def build_prompt(self, query: str, context: Dict) -> str:
        """Build the final prompt string.

        Args:
        ----
            query: User message.
            context: Domain-specific context.

        Returns:
        -------
            Full formatted prompt string.

        """
        raise NotImplementedError
