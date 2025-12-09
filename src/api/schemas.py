"""Module: schemas.

Pydantic models for API requests and responses.
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str
    selected_domain: str | None = None



class ChatResponse(BaseModel):
    session_id: str
    response: str
    domain: str
    confidence: float
