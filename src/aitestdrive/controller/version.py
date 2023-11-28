import logging
import os

from fastapi import APIRouter
from pydantic import BaseModel

log = logging.getLogger(__name__)

api = APIRouter(prefix="/version", tags=["Version info"])


class ServiceInfo(BaseModel):
    service_name: str
    service_revision: str


@api.get("")
async def chat() -> ServiceInfo:
    log.debug(f"Version request received.")

    service_name = os.environ.get('K_SERVICE', 'Unknown')
    service_revision = os.environ.get('K_REVISION', 'Unknown')

    return ServiceInfo(
        service_name=service_name,
        service_revision=service_revision
    )
