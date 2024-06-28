from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from homelab import get_templates
from homelab.bg import (drop_bg_items_table, find_bg_item,
                        get_gear_locator_items, list_bg_items)

PREFIX = "/bg"

router = APIRouter(prefix=PREFIX)


@router.get("/", response_description="Just a hello world")
async def home(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("bg.html", context={'request': request})


@router.get("/search_items", response_description="item search",  response_class=HTMLResponse)
async def search_items(request: Request, query: str, templates: Jinja2Templates = Depends(get_templates)):
    items = await find_bg_item(query)
    return templates.TemplateResponse("bg-gear-search.html", context={'request': request, 'items': items})


@router.get("/populate_gear_locator", response_class=HTMLResponse)
async def polulate_gear_locator():
    await get_gear_locator_items()
    items = await list_bg_items()
    return f"items: {items}"


@router.get("/list_gear",  response_class=HTMLResponse)
async def list_gear_locator_items():
    await drop_bg_items_table()
    await get_gear_locator_items()
    items = await list_bg_items()
    return f"items: {items}"


@router.get("/delete_gear_table",  response_class=HTMLResponse)
async def delete_gear_table():
    await drop_bg_items_table()
