from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pokemon.depends import get_templates
from pokemon.models import Pokemon

from .utils import find_pokemon

PREFIX = ""

router = APIRouter(prefix=PREFIX)


@router.get("/", response_description="pokemon home page")
async def pokemon_home(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("index.html", context={'request': request})


@router.get("/search", response_class=HTMLResponse)
async def search(request: Request, query: str,  templates: Jinja2Templates = Depends(get_templates)):
    pokemon: List[Pokemon] = await find_pokemon(query)

    return templates.TemplateResponse("search-results.html", context={'request': request, 'pokemon': pokemon})
