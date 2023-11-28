import logging
import os

from fastapi import APIRouter

log = logging.getLogger(__name__)

api = APIRouter(prefix="/version", tags=["Version info"])


@api.get("")
async def chat() -> str:
    log.debug(f"Version request received.")

    service_name = os.environ.get('K_SERVICE')
    service_revision = os.environ.get('K_REVISION')

    return f"""Running!
    Service name: {service_name}
    Service revision: {service_revision}
"""
