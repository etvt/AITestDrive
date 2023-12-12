import logging
from typing import List

import vertexai
from fastapi import Depends
from vertexai.language_models import ChatModel

from aitestdrive.common.models import ChatMessage
from aitestdrive.service.document import DocumentService

log = logging.getLogger(__name__)


class ChatService:
    def __init__(self, document_service=Depends(DocumentService)):
        self.__document_service = document_service

    async def reply(self, history: List[ChatMessage]) -> ChatMessage:
        new_message = history[-1].content

        documents = await self.__document_service.search_documents(new_message)

        chat_model = ChatModel.from_pretrained("chat-bison@001")
        chat_session = chat_model.start_chat(
            context="Your name is 'XYZ company assistant'. Your job is to answer questions related to the company XYZ."
                    f" Additionally, here are some snippets from related documents: {documents} " if documents else "",
            message_history=convert_history(history[:-1]),
            temperature=0.1,
            max_output_tokens=256,
            top_p=0.8,
            top_k=40
        )

        response = await chat_session.send_message_async(new_message)
        log.debug(f"Response from Model: {response.text}")

        return ChatMessage(content=response.text, role='assistant')


def convert_history(history: List[ChatMessage]) -> List[vertexai.language_models.ChatMessage]:
    return [vertexai.language_models.ChatMessage(content=message.content, author=message.role) for message in history]
