from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ChatRequest(BaseModel):
    token: str
    prompt: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str