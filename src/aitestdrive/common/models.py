from typing import List, Literal

from pydantic import BaseModel


class ChatMessage(BaseModel):
    content: str
    role: Literal['assistant', 'user']


class ChatRequest(BaseModel):
    history: List[ChatMessage] = []
