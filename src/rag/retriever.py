"""Module: retriever.

High-level interface for retrieving top chunks for a query.
"""

from typing import List

from src.rag.embedder import Embedder
from src.rag.vectorstore import VectorStore


class Retriever:
    """Retriever that embeds queries and returns top chunks from FAISS."""

    def __init__(self, embedder: Embedder, store: VectorStore) -> None:
        self.embedder = embedder
        self.store = store

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        """Retrieve top-k chunks related to query.

        Args:
        ----
            query: Query text.
            k: Number of chunks.

        Returns:
        -------
            List of retrieved chunks.

        """
        q_vec = self.embedder.embed_one(query)
        results = self.store.search(q_vec, k=k)
        return [chunk for chunk, _distance in results]
