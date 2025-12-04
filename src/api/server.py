"""Module: server
FastAPI backend for the Multi-Domain LLM Assistant with RAG & streaming.
"""

from __future__ import annotations

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from src.api.deps import get_assistant
from src.api.schemas import ChatRequest, ChatResponse
from src.api.upload import router as upload_router

# --------------------- FASTAPI APP ---------------------

app = FastAPI(
    title="Multi-Domain LLM Assistant API",
    description="Backend for multi-agent LLM system with RAG + WebSocket streaming.",
    version="1.0.0",
)


# --------------------- CORS ----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------- INCLUDE UPLOAD ROUTER ------------

app.include_router(upload_router, prefix="/upload")


# --------------------- HEALTH CHECK ---------------------


@app.get("/health")
def health():
    return {"status": "ok"}


# --------------------- REST CHAT ENDPOINT ---------------


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Standard chat endpoint using REST."""
    assistant = get_assistant()
    output = assistant.ask(req.message)

    domain, confidence = extract_domain_meta(output)
    clean_output = strip_domain_meta(output)

    return ChatResponse(
        session_id=req.session_id,
        response=clean_output,
        domain=domain,
        confidence=confidence,
    )


# --------------------- WEBSOCKET STREAMING --------------


@app.websocket("/stream")
async def stream_chat(websocket: WebSocket):
    """Real-time streaming chat endpoint.
    Sends line-by-line chunks ending with [[END]].
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


# --------------------- HELPERS --------------------------


def extract_domain_meta(text: str):
    """Extract domain + confidence from the header:
    [domain=education confidence=0.92]
    """
    try:
        header = text.split("\n")[0].strip()
        if not header.startswith("[domain="):
            return "unknown", 0.0

        domain = header.split("domain=")[1].split(" ")[0]
        conf = float(header.split("confidence=")[1].split("]")[0])
        return domain, conf
    except Exception:
        return "unknown", 0.0


def strip_domain_meta(text: str):
    """Remove header so UI sees clean content."""
    lines = text.split("\n")
    if lines and lines[0].startswith("[domain="):
        return "\n".join(lines[1:]).strip()
    return text.strip()


# --------------------- ENTRY POINT ----------------------

if __name__ == "__main__":
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
