"""RAG Pipeline — loads → chunks → embeds → indexes → retrieves"""

from __future__ import annotations
from typing import List

from src.rag.loader import DocumentLoader
from src.rag.vectorstore import VectorStore


class RAGPipeline:
    """Full RAG pipeline wrapper."""

    def __init__(self) -> None:
        self.loader = DocumentLoader()
        self.vectorstore = VectorStore()
        self.ready = False

    def add_documents(self, paths: List[str]) -> None:
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
        if not self.ready:
            return []
        return self.vectorstore.query(question, top_k)
