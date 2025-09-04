from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.settings import settings
from app.depends import templates
from app.logger import logger

from datetime import datetime

PREFIX = "/manifests"

router = APIRouter(prefix=PREFIX)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # example settings call
    host = settings.api_host

    # example log
    logger.debug(f"Index called {host=}")

    time = str(datetime.now())

    context = {
        "request": request,
        "time": time
    }

    return templates.TemplateResponse("index.html.j2", context=context)
