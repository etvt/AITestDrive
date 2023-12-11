import io
import logging
from typing import List

import pdfplumber
from fastapi import Depends
from google.cloud import storage
from langchain.text_splitter import TokenTextSplitter
from vertexai.language_models import TextEmbeddingModel

from aitestdrive.common.config import config
from aitestdrive.di import singletons
from aitestdrive.di.factories import create_storage_client
from aitestdrive.persistence.qdrant import QdrantService

log = logging.getLogger(__name__)


class DocumentService:

    def __init__(self,
                 storage_client: storage.Client = Depends(create_storage_client),
                 qdrant_service: QdrantService = Depends(singletons.depends(QdrantService))):
        self.__storage_client = storage_client
        self.__qdrant_service = qdrant_service
        self.__embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko")

    async def search_documents(self, query: str, limit: int = 5) -> List[str]:
        query_vector = (await self.__embedding_model.get_embeddings_async([query]))[0].values

        search_results = await self.__qdrant_service.search(query_vector, limit=limit)

        return [payload['text'] for payload in search_results]

    async def re_vectorize_documents_from_storage(self):
        bucket = self.__storage_client.bucket(config.document_bucket)

        chunks = []
        for blob in bucket.list_blobs():
            if blob.name.endswith('.pdf'):
                pdf_file_content = io.BytesIO(blob.download_as_bytes())
                pdf_as_text = DocumentService.extract_text_from_pdf(pdf_file_content)
                chunks += DocumentService.chunk_text(pdf_as_text, chunk_size=300, chunk_overlap=10)

        embeddings = await self.__embedding_model.get_embeddings_async(chunks)
        assert len(embeddings) > 0

        await self.__qdrant_service.re_upload_collection(vector_size=len(embeddings[0].values),
                                                         vectors=map(lambda embedding: embedding.values, embeddings),
                                                         payloads=map(lambda chunk: {'text': chunk}, chunks))

    @staticmethod
    def extract_text_from_pdf(pdf_file_content):
        with pdfplumber.open(pdf_file_content) as pdf:
            return '\n\n\n'.join(
                [page.extract_text() for page in pdf.pages]
            )

    @staticmethod
    def chunk_text(text, chunk_size, chunk_overlap) -> List[str]:
        text_splitter = TokenTextSplitter(chunk_size=chunk_size,
                                          chunk_overlap=chunk_overlap)

        return [doc.page_content for doc in text_splitter.create_documents([text])]
