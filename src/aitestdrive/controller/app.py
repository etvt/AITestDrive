import logging
import time

from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from aitestdrive.controller.chat import api as chat_api
from aitestdrive.controller.document import api as documents_api
from aitestdrive.controller.version import api as version_api

log = logging.getLogger(__name__)

api = FastAPI(docs_url="/api/docs", redoc_url=None)

# CORS Middleware
origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    log.info(f"Request received: {request.method} {request.url.path} | Time: {str(process_time)}")
    return response


api_router = APIRouter(prefix="/api")
api_router.include_router(chat_api)
api_router.include_router(documents_api)
api_router.include_router(version_api)

api.include_router(api_router)
