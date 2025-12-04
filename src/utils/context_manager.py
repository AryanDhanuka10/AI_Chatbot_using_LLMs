"""Module: context_manager.

Maintains short-term conversation memory and structured context
for RAG + LLM prompting.
"""

from __future__ import annotations

from typing import Dict, List


class ContextManager:
    """Stores user/assistant message history and builds
    structured context for agents.
    """

    def __init__(self) -> None:
        self.memory: List[str] = []
        self.state: Dict = {}

    def add_memory(self, user_msg: str, assistant_msg: str) -> None:
        """Add the latest user + assistant messages to memory."""
        self.memory.append(f"User: {user_msg}")
        self.memory.append(f"Assistant: {assistant_msg}")

        # Keep memory bounded (prevents prompt explosion)
        if len(self.memory) > 12:
            self.memory = self.memory[-12:]

    def build_context(self) -> Dict:
        """Build structured context dictionary expected by agents."""
        return {
            "memory": self.memory,
            "state": self.state,
        }

    def clear(self) -> None:
        """Reset full memory and state."""
        self.memory = []
        self.state = {}
