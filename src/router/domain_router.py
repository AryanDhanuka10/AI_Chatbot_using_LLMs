"""
Stable Domain Router (NEVER returns invalid output)

This router safely classifies queries into domains using an LLM.
It ALWAYS returns a valid dictionary and NEVER throws a 500 error.
"""

from __future__ import annotations

import json
import logging
from typing import Dict, List, Optional

from src.models.llm import LLM


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class DomainRouter:
    """Rock-solid router that NEVER breaks."""

    def __init__(
        self,
        domains: Optional[List[str]] = None,
        llm: Optional[LLM] = None,
        system_instruction: str | None = None,
    ) -> None:

        self.domains = domains or [
            "education",
            "coding",
            "medical",
            "legal",
            "general",
        ]

        self.llm = llm or LLM()

        self.system_instruction = system_instruction or (
            "You classify user messages. "
            "Respond ONLY in strict JSON with keys: domain, confidence, reason. "
            "Never include anything outside the JSON."
        )

    # ---------------------------------------------------------
    # Prompt Builder
    # ---------------------------------------------------------
    def _prompt(self, query: str) -> str:
        """Build safe few-shot JSON classification prompt."""
        allowed = ", ".join(self.domains)

        examples = (
            "Example:\n"
            "User: 'How do I use BFS?'\n"
            'JSON: {"domain": "education", "confidence": 0.95, '
            '"reason": "algorithm explanation"}\n\n'
        )

        return (
            f"{self.system_instruction}\n\n"
            f"Allowed domains: {allowed}\n\n"
            f"{examples}"
            f"User: '{query}'\n"
            "JSON:"
        )

    # ---------------------------------------------------------
    # Main Router
    # ---------------------------------------------------------
    def route(self, query: str) -> Dict:
        """Classify query into a domain. ALWAYS returns a valid dict."""
        prompt = self._prompt(query)

        try:
            raw = self.llm.generate(prompt, max_tokens=120).strip()

            # Extract JSON safely
            start = raw.find("{")
            end = raw.rfind("}")

            if start == -1 or end == -1:
                raise ValueError("No JSON found in LLM output")

            json_text = raw[start : end + 1]
            data = json.loads(json_text)

            domain = str(data.get("domain", "")).lower()
            confidence = float(data.get("confidence", 0.0))
            reason = data.get("reason", "LLM output")

            if domain not in self.domains:
                raise ValueError(f"Invalid domain: {domain}")

            return {
                "domain": domain,
                "confidence": confidence,
                "reason": reason,
            }

        except Exception as err:
            LOGGER.warning(f"Router fallback triggered: {err}")
            return self._fallback(query)

    # ---------------------------------------------------------
    # Fallback Logic (Guarantees no crash)
    # ---------------------------------------------------------
    def _fallback(self, query: str) -> Dict:
        """Guaranteed-safe fallback using keyword heuristics."""
        q = query.lower()

        # Coding
        if any(word in q for word in ["error", "bug", "debug", "code", "compile"]):
            return {"domain": "coding", "confidence": 0.0, "reason": "keyword fallback"}

        # Legal
        if any(word in q for word in ["contract", "legal", "law", "court", "ipc"]):
            return {"domain": "legal", "confidence": 0.0, "reason": "keyword fallback"}

        # Medical
        if any(word in q for word in ["fever", "symptom", "disease", "bp", "pain"]):
            return {"domain": "medical", "confidence": 0.0, "reason": "keyword fallback"}

        # Education
        if any(word in q for word in ["explain", "learn", "study", "homework"]):
            return {"domain": "education", "confidence": 0.0, "reason": "keyword fallback"}

        # General fallback
        return {"domain": "general", "confidence": 0.0, "reason": "fallback default"}
