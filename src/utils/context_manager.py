"""Module: context_manager.

Simple context manager for agents to store domain-specific memory/state.
"""

from typing import Dict, List


class ContextManager:
    """Manages conversation memory and domain context."""

    def __init__(self) -> None:
        """Initialize empty memory and state containers."""
        self.memory: List[str] = []
        self.state: Dict = {}

    def add_memory(self, text: str) -> None:
        """Append new conversation info to memory."""
        self.memory.append(text)

    def get_context(self) -> Dict:
        """Return memory and state in a dictionary."""
        return {"memory": self.memory, "state": self.state}

    def reset(self) -> None:
        """Clear all stored context."""
        self.memory.clear()
        self.state.clear()
