import io
import logging
from typing import List

import pdfplumber
from google.cloud import storage
from langchain.text_splitter import TokenTextSplitter
from vertexai.language_models import TextEmbeddingModel

from aitestdrive.common.async_locks import ReadWriteLock
from aitestdrive.common.config import config
from aitestdrive.persistence.qdrant import qdrant_service

log = logging.getLogger(__name__)


class DocumentService:

    def __init__(self):
        self.__storage_client = storage.Client()
        self.__embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko")
        self.__lock = ReadWriteLock()

    async def search_documents(self, query: str, limit: int = 5) -> List[str]:
        query_vector = (await self.__embedding_model.get_embeddings_async([query]))[0].values

        async with self.__lock.reader():
            search_results = await qdrant_service.search(query_vector, limit=limit)

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

        async with self.__lock.writer():
            await qdrant_service.re_upload_collection(vector_size=len(embeddings[0].values),
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


document_service = DocumentService()
