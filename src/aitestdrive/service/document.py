import logging
from typing import List

from fastapi import Depends
from langchain.document_loaders import GCSDirectoryLoader
from langchain.text_splitter import TokenTextSplitter
from langchain_core.documents import Document

from aitestdrive.di import singletons
from aitestdrive.di.factories import create_gcs_directory_loader, create_qdrant_service
from aitestdrive.persistence.qdrant import QdrantService, QdrantReadContext

log = logging.getLogger(__name__)


class DocumentService:

    def __init__(self,
                 storage_directory_loader: GCSDirectoryLoader = Depends(create_gcs_directory_loader),
                 qdrant_service: QdrantService = Depends(singletons.of(create_qdrant_service))):
        self.__storage_directory_loader = storage_directory_loader
        self.__qdrant_service = qdrant_service

    async def search_documents(self, query: str, limit: int = 5) -> List[str]:
        async with self.read_context() as context:
            search_results = await context.search(query, limit=limit)
            return [doc.page_content for doc in search_results]

    def read_context(self) -> QdrantReadContext:
        return self.__qdrant_service.read_context()

    async def re_vectorize_documents_from_storage(self):
        docs = self.__storage_directory_loader.load()
        assert len(docs) > 0
        chunks = DocumentService.chunk_documents(docs)

        await self.__qdrant_service.re_upload_collection(chunks)

    @staticmethod
    def chunk_documents(documents, chunk_size=300, chunk_overlap=10) -> List[Document]:
        text_splitter = TokenTextSplitter(chunk_size=chunk_size,
                                          chunk_overlap=chunk_overlap)

        return text_splitter.split_documents(documents)
