"""Module: base_agent.

Defines BaseAgent for structured LLM interaction:
- Optional RAG enrichment
- Domain-specific prompt templates
- Unified LLM generate() interface
"""

from __future__ import annotations

from typing import Dict, List, Optional

from src.agents.prompts.base_prompt import BasePromptTemplate
from src.models.llm import LLM


class BaseAgent:
    """Abstract base class for all domain agents.

    Responsibilities:
    - Build prompts using the domain prompt template.
    - Optionally enrich queries using RAG retrieved context.
    - Invoke the LLM and return structured output.
    """

    def __init__(
        self,
        prompt_template: BasePromptTemplate,
        rag: Optional[object] = None,
    ) -> None:
        """Initialize an agent with its domain-specific prompt template.

        Args:
        ----
            prompt_template: Domain-specific builder implementing build_prompt().
            rag: Optional RAG pipeline (must expose query(text) -> List[str]).

        """
        self.llm = LLM()
        self.prompt_template = prompt_template
        self.rag = rag

    def enable_rag(self, rag_pipeline) -> None:
        """Attach a RAG pipeline to this agent at runtime.

        Args:
        ----
            rag_pipeline: Object exposing .query(text) -> List[str].

        """
        self.rag = rag_pipeline

    def run(self, query: str, context: Optional[Dict] = None) -> str:
        """Execute the full agent pipeline:
        1. RAG retrieval (optional)
        2. Prompt construction
        3. LLM call

        Args:
        ----
            query: Incoming user question.
            context: Memory + agent state dictionary.

        Returns:
        -------
            str: The LLM-generated output.

        """
        enriched_query = query

        if self.rag is not None:
            try:
                retrieved_chunks: List[str] = self.rag.query(query)
                if retrieved_chunks:
                    knowledge = "\n\n".join(retrieved_chunks)
                    enriched_query = (
                        f"Relevant Knowledge:\n{knowledge}\n\n" f"User Query:\n{query}"
                    )
            except Exception as exc:
                # Fail gracefully — never break the pipeline
                enriched_query = (
                    f"[RAG Retrieval Failed: {exc}]\n\nUser Query:\n{query}"
                )

        prompt = self.prompt_template.build_prompt(
            enriched_query,
            context or {},
        )

        return self.llm.generate(prompt)
