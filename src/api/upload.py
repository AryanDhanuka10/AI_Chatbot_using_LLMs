"""Module: upload

File upload endpoint for RAG ingestion.
Supports PDF and TXT documents.
"""

from __future__ import annotations

import os

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from src.rag.loader import DocumentLoader

router = APIRouter()
UPLOAD_DIR = "uploaded_docs"


# Ensure folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_files(files: list[UploadFile] = File(...)):
    """Upload PDF/TXT files → save → parse → return extracted text length.

    Example Response:
        {
            "filename": "doc.pdf",
            "saved_to": "uploaded_docs/doc.pdf",
            "chunks": 12
        }
    """
    results = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Load & split text
        try:
            loader = DocumentLoader()
            chunks = loader.load(file_path)
            results.append(
                {
                    "filename": file.filename,
                    "saved_to": file_path,
                    "chunks": len(chunks),
                }
            )
        except Exception as e:
            results.append(
                {
                    "filename": file.filename,
                    "error": str(e),
                }
            )

    return JSONResponse(content={"uploads": results})
