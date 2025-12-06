"""Base Prompt Template (Abstract Class)"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict


class BasePromptTemplate(ABC):
    """All domain prompt templates must extend this class."""

    @abstractmethod
    def build_prompt(self, query: str, context: Dict) -> str:
        """Build final LLM prompt using query + context."""
        raise NotImplementedError
