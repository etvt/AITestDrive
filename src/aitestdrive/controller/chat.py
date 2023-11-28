import logging

from fastapi import APIRouter, Body
from google.cloud import aiplatform
from vertexai.language_models import TextGenerationModel

log = logging.getLogger(__name__)

api = APIRouter(prefix="/chat", tags=["Chat"])

aiplatform.init()


@api.post("/")
async def chat(request: str = Body()) -> str:
    log.debug(f"Request received: '{request}'")
    return await answer_question_using_ai(request)


async def answer_question_using_ai(request: str) -> str:
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = await model.predict_async(
        request,
        temperature=0.1,
        max_output_tokens=256,
        top_p=0.8,
        top_k=40
    )
    log.debug(f"Response from Model: {response.text}")

    return response.text
