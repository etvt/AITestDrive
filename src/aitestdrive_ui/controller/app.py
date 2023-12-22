from importlib import resources

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates

import aitestdrive_ui.resources
from aitestdrive_ui.common.config import config

app = FastAPI()

resources_dir = resources.files(aitestdrive_ui.resources)
with resources.as_file(resources_dir.joinpath("static")) as static_dir:
    app.mount("/static", StaticFiles(directory=static_dir))

with resources.as_file(resources_dir.joinpath("templates")) as templates_dir:
    templates = Jinja2Templates(directory=templates_dir)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "chat_api_url": config.chat_api_url})
