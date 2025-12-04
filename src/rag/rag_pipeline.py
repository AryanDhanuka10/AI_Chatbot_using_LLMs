"""Module: rag_pipeline

Coordinator for DocumentLoader + VectorStore.
Provides `add_documents()` and `query()` for RAG-enabled agents.
"""

from __future__ import annotations

from typing import List

from src.rag.loader import DocumentLoader
from src.rag.vectorstore import VectorStore


class RAGPipeline:
    """Full RAG pipeline: load → chunk → embed → index → retrieve."""

    def __init__(self) -> None:
        self.loader = DocumentLoader()
        self.vectorstore = VectorStore()
        self.ready = False

    def add_documents(self, paths: List[str]) -> None:
        """Load & index multiple documents."""
        all_chunks = []

        for p in paths:
            chunks = self.loader.load(p)
            all_chunks.extend(chunks)

        if not all_chunks:
            self.ready = False
            return

        self.vectorstore.build(all_chunks)
        self.ready = True

    def query(self, question: str, top_k: int = 5) -> List[str]:
        """Retrieve most relevant chunks for a question."""
        if not self.ready:
            return []

        return self.vectorstore.query(question, top_k=top_k)
