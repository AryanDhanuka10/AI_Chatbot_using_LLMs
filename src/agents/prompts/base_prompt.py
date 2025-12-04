"""Module: base_prompt.

Defines BasePromptTemplate — the abstract class all domain prompt templates
must extend. It standardizes the interface for constructing structured prompts.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class BasePromptTemplate(ABC):
    """Abstract base class for domain prompt templates.

    Each child class must implement build_prompt(), which receives:
    - query: (str) enriched or raw user query
    - context: (dict) memory/state provided by ContextManager
    """

    @abstractmethod
    def build_prompt(self, query: str, context: Dict) -> str:
        """Construct a full LLM prompt using query + context.

        Args:
        ----
            query: The user's message, possibly enriched with RAG context.
            context: Dict containing memory/state.

        Returns:
        -------
            str: Final prompt string to feed into the LLM.

        """
        raise NotImplementedError
