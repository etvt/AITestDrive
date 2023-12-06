import logging
from typing import List

import vertexai
from fastapi import APIRouter
from google.cloud import aiplatform
from vertexai.language_models import ChatModel

from aitestdrive.common.config import config
from aitestdrive.common.models import ChatMessage, ChatRequest

log = logging.getLogger(__name__)

api = APIRouter(prefix="/chat", tags=["Chat"])

aiplatform.init(project=config.gcp_project)


@api.post("/")
async def chat(request: ChatRequest) -> ChatMessage:
    log.debug(f"Request received: '{request}'")
    assert len(request.history) >= 1

    chat_model = ChatModel.from_pretrained("chat-bison@001")

    message = request.history[-1]

    chat_session = chat_model.start_chat(
        context="Your name is 'XYZ company assistant'. Your job is to answer questions related to the company XYZ.",
        message_history=convert_history(request.history[:-1])
    )

    response = chat_session.send_message(
        message.content,
        temperature=0.1,
        max_output_tokens=256,
        top_p=0.8,
        top_k=40
    )
    log.debug(f"Response from Model: {response.text}")

    return ChatMessage(content=response.text, role='assistant')


def convert_history(history: List[ChatMessage]) -> List[vertexai.language_models.ChatMessage]:
    return [vertexai.language_models.ChatMessage(content=message.content, author=message.role) for message in history]
