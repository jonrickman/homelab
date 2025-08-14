from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from journal.depends import get_templates

PREFIX = ""

router = APIRouter(prefix=PREFIX)


@router.get("/", response_description="journal home page")
async def read_root(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("index.html", context={'request': request})


