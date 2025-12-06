"""Document Loader — PDF + TXT → clean text chunks."""

from __future__ import annotations

import logging
import os
from typing import List

from PyPDF2 import PdfReader

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class DocumentLoader:
    """Loads documents and splits into chunks."""

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

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

        return self._chunk(text)

    def _load_pdf(self, path: str) -> str:
        LOGGER.info(f"Loading PDF: {path}")
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    def _load_txt(self, path: str) -> str:
        LOGGER.info(f"Loading TXT: {path}")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def _chunk(self, text: str) -> List[str]:
        if not text.strip():
            return []

        words = text.split()
        chunks = []
        chunk = []

        curr_len = 0

        for word in words:
            if curr_len + len(word) > self.chunk_size:
                chunks.append(" ".join(chunk))
                chunk = chunk[-self.chunk_overlap :]  # overlap
                curr_len = sum(len(w) for w in chunk)

            chunk.append(word)
            curr_len += len(word)

        if chunk:
            chunks.append(" ".join(chunk))

        return chunks
