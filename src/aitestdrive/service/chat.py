import logging
from typing import List

from fastapi import Depends
from langchain_core.language_models import BaseLLM
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage

from aitestdrive.common.models import ChatMessage
from aitestdrive.di.factories import create_llm
from aitestdrive.service.document import DocumentService
from aitestdrive.service.langchain.chains import create_conversational_qa_chain

log = logging.getLogger(__name__)


class ChatService:
    def __init__(self,
                 document_service: DocumentService = Depends(),
                 llm: BaseLLM = Depends(create_llm)):
        self.__document_service = document_service
        self.__llm = llm

    async def reply(self, history: List[ChatMessage]) -> ChatMessage:
        async with self.__document_service.read_context() as context:
            conversational_qa_chain = create_conversational_qa_chain(self.__llm, context.as_retriever())
            response: str = await conversational_qa_chain.ainvoke({
                'question': history[-1].content,
                'chat_history': convert_history(history[:-1])
            })

        log.debug(f"Response from Model: {response}")

        return ChatMessage(content=response, role='assistant')


def convert_history(history: List[ChatMessage]) -> List[BaseMessage]:
    return [HumanMessage(content=message.content) if message.role == 'user'
            else AIMessage(content=message.content)
            for message in history]
