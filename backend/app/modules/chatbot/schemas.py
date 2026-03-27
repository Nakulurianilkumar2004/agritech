# app/modules/crop_chatbot/schemas.py
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    mode: Optional[str] = "text"  # "text" or "voice"

class ChatResponse(BaseModel):
    response: str
    audio: Optional[str] = None