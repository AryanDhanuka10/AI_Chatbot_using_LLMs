"""Module: vectorstore

FAISS-based vector store using SentenceTransformer embeddings.
"""

from __future__ import annotations

from typing import List

import faiss
from sentence_transformers import SentenceTransformer


class VectorStore:
    """Stores embeddings + FAISS index and performs similarity search."""

    def __init__(self, embed_model: str = "all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(embed_model)
        self.index = None
        self.text_chunks: List[str] = []

    def build(self, chunks: List[str]) -> None:
        """Build FAISS index from text chunks."""
        self.text_chunks = chunks

        embeddings = self.model.encode(chunks, convert_to_numpy=True)
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def query(self, query: str, top_k: int = 5) -> List[str]:
        """Return top-k matching text chunks."""
        if self.index is None:
            return []

        q_emb = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(q_emb, top_k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.text_chunks):
                results.append(self.text_chunks[idx])

        return results
