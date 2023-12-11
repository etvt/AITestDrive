import logging

from fastapi import APIRouter, Depends

from aitestdrive.service.document import DocumentService

log = logging.getLogger(__name__)

api = APIRouter(prefix="/documents", tags=["Documents"])


@api.post("/re-vectorize-from-storage")
async def re_vectorize_documents_from_storage(document_service=Depends(DocumentService)):
    log.info(f"Request received to re-vectorize documents from storage")
    await document_service.re_vectorize_documents_from_storage()
    log.info("Re-vectorization of documents done.")
