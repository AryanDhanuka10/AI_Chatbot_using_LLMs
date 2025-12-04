"""Module: deps.

Holds global dependency objects like the singleton MultiDomainAssistant.
"""

from functools import lru_cache

from src.main import MultiDomainAssistant


@lru_cache(maxsize=1)
def get_assistant() -> MultiDomainAssistant:
    """Return singleton assistant instance."""
    return MultiDomainAssistant()
