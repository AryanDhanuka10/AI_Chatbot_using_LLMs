"""
Module: server

FastAPI backend for the Multi-Domain LLM Assistant
with RAG support and WebSocket streaming.
"""

from __future__ import annotations

import os
import sys
import uvicorn

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# ==========================================================
# PATH FIX (for deployment & local execution consistency)
# ==========================================================

# Absolute path of this file: .../src/api/server.py
CURRENT_FILE = os.path.abspath(__file__)

# Move up to project root
ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(CURRENT_FILE)
    )
)

# Ensure "src" is discoverable
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# ==========================================================
# INTERNAL IMPORTS
# ==========================================================

from src.api.deps import get_assistant
from src.api.schemas import ChatRequest, ChatResponse
from src.api.upload import router as upload_router

# ==========================================================
# FASTAPI APP CONFIG
# ==========================================================

app = FastAPI(
    title="Multi-Domain LLM Assistant API",
    description="Backend for a modular multi-agent LLM system with RAG and streaming.",
    version="1.0.0",
)

# ==========================================================
# CORS CONFIG
# IMPORTANT: This FIXES your frontend fetch error
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://ai-chatbot-using-ll-ms.vercel.app",
        "https://ai-chatbot-using-llms.vercel.app",
        "*",  # keep for now; restrict later
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# ROUTERS
# ==========================================================

# RAG document upload
app.include_router(upload_router, prefix="/upload")

# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/health")
def health():
    return {"status": "ok"}

# ==========================================================
# REST CHAT ENDPOINT
# ==========================================================

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    assistant = get_assistant()

    output = assistant.ask(
        req.message,
        selected_domain=req.selected_domain,
    )

    domain, confidence = extract_domain_meta(output)
    clean_output = strip_domain_meta(output)

    return ChatResponse(
        session_id=req.session_id,
        response=clean_output,
        domain=domain,
        confidence=confidence,
    )

# ==========================================================
# WEBSOCKET STREAMING ENDPOINT
# ==========================================================

@app.websocket("/stream")
async def stream_chat(websocket: WebSocket):
    """
    Real-time streaming endpoint.
    Sends responses line-by-line and terminates with [[END]].
    """
    await websocket.accept()
    assistant = get_assistant()

    try:
        while True:
            req = await websocket.receive_json()
            message = req.get("message", "").strip()

            if not message:
                await websocket.send_text("[[ERROR: empty message]]")
                continue

            full_output = assistant.ask(message)

            for line in full_output.split("\n"):
                if line.strip():
                    await websocket.send_text(line)

            await websocket.send_text("[[END]]")

    except WebSocketDisconnect:
        print("WebSocket disconnected")

# ==========================================================
# METADATA PARSING HELPERS
# ==========================================================

def extract_domain_meta(text: str):
    """
    Extract domain + confidence from:
    [domain=education confidence=0.92]
    """
    try:
        header = text.split("\n")[0].strip()

        if not header.startswith("[domain="):
            return "unknown", 0.0

        domain = header.split("domain=")[1].split(" ")[0]
        confidence = float(
            header.split("confidence=")[1].split("]")[0]
        )

        return domain, confidence

    except Exception:
        return "unknown", 0.0


def strip_domain_meta(text: str):
    """
    Removes metadata header so UI sees clean output.
    """
    lines = text.split("\n")

    if lines and lines[0].startswith("[domain="):
        return "\n".join(lines[1:]).strip()

    return text.strip()

# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
