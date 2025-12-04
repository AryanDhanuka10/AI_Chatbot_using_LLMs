"""Module: schemas.

Pydantic models for API requests and responses.
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    domain: str
    confidence: float
