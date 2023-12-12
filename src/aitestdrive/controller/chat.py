import logging

from fastapi import APIRouter, Depends

from aitestdrive.common.models import ChatMessage, ChatRequest
from aitestdrive.service.chat import ChatService

log = logging.getLogger(__name__)

api = APIRouter(prefix="/chat", tags=["Chat"])


@api.post("/")
async def chat(request: ChatRequest,
               chat_service=Depends(ChatService)) -> ChatMessage:
    log.debug(f"Request received: '{request}'")
    assert len(request.history) > 0

    return await chat_service.reply(request.history)
