import logging

from fastapi import APIRouter, Body

log = logging.getLogger(__name__)

api = APIRouter(prefix="/chat", tags=["Chat"])


@api.post("/")
async def chat(request: str = Body()) -> str:
    log.debug(f"Request received: '{request}'")
    return f"Echo! {request}. Done."
