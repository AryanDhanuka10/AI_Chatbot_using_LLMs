"""Module: loader

Loads documents (PDF, TXT) and splits them into clean text chunks
for embedding + FAISS indexing.
"""

from __future__ import annotations

import logging
import os
from typing import List

from PyPDF2 import PdfReader

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class DocumentLoader:
    """Simple loader for PDFs and plain text files."""

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    # Load a single file
    def load(self, path: str) -> List[str]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Document not found: {path}")

        ext = path.lower().split(".")[-1]

        if ext == "pdf":
            text = self._load_pdf(path)
        elif ext in ("txt", "md"):
            text = self._load_txt(path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        return self._split_into_chunks(text)

    def _load_pdf(self, path: str) -> str:
        LOGGER.info(f"Loading PDF: {path}")
        reader = PdfReader(path)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    def _load_txt(self, path: str) -> str:
        LOGGER.info(f"Loading text file: {path}")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def _split_into_chunks(self, text: str) -> List[str]:
        """Basic chunking without LangChain."""
        if not text.strip():
            return []

        chunks = []
        words = text.split()

        current = []
        length = 0

        for w in words:
            if length + len(w) > self.chunk_size:
                chunks.append(" ".join(current))
                current = current[-self.chunk_overlap // 5 :]  # word-level overlap
                length = sum(len(x) for x in current)

            current.append(w)
            length += len(w)

        if current:
            chunks.append(" ".join(current))

        return chunks
