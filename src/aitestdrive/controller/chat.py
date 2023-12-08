import logging
from typing import List

import vertexai
from fastapi import APIRouter
from vertexai.language_models import ChatModel

from aitestdrive.common.models import ChatMessage, ChatRequest
from aitestdrive.service.document import document_service

log = logging.getLogger(__name__)

api = APIRouter(prefix="/chat", tags=["Chat"])


@api.post("/")
async def chat(request: ChatRequest) -> ChatMessage:
    log.debug(f"Request received: '{request}'")

    assert len(request.history) > 0
    new_message = request.history[-1].content

    documents = await document_service.search_documents(new_message)

    chat_model = ChatModel.from_pretrained("chat-bison@001")
    chat_session = chat_model.start_chat(
        context="Your name is 'XYZ company assistant'. Your job is to answer questions related to the company XYZ."
                f" Additionally, here are some snippets from related documents: {documents} " if documents else "",
        message_history=convert_history(request.history[:-1])
    )

    response = await chat_session.send_message_async(
        new_message,
        temperature=0.1,
        max_output_tokens=256,
        top_p=0.8,
        top_k=40
    )
    log.debug(f"Response from Model: {response.text}")

    return ChatMessage(content=response.text, role='assistant')


def convert_history(history: List[ChatMessage]) -> List[vertexai.language_models.ChatMessage]:
    return [vertexai.language_models.ChatMessage(content=message.content, author=message.role) for message in history]
