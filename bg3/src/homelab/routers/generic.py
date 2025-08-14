from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from homelab.depends import get_templates

PREFIX = ""

router = APIRouter()


@router.get("/", response_description="Just a hello world")
async def home(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("index.html", context={'request': request, 'name': "Jeff"})
