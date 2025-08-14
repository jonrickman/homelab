from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from homelab.die import calculate_odds
from homelab.depends import get_templates
from homelab.bg import (drop_bg_items_table, find_bg_item,
                        get_gear_locator_items, list_bg_items, list_bg_mods, populate_bg_mods)

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


@router.get("/get_modlist", response_description="display mod list",  response_class=HTMLResponse)
async def get_mod_list(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    mods = await list_bg_mods()
    return templates.TemplateResponse("bg-gear-search.html", context={'request': request, 'mods': mods})


@router.post('/roll')
async def roll_die(request: Request, die_str: str = Form(), target: str = Form(),  templates: Jinja2Templates = Depends(get_templates)):
    print(f"{die_str=}, {target=}")
    probability, favorable_outcomes, total_outcomes = calculate_odds(die_str, int(target))

    return templates.TemplateResponse("bg-calculator-results.html", context={
        'request': request,
        'probability': probability,
        'favorable_outcomes': favorable_outcomes,
        'total_outcomes': total_outcomes})


# Leaving in for debug
@router.get("/list_gear",  response_class=HTMLResponse)
async def list_gear_locator_items():
    items = await list_bg_items()
    return f"items: {items}"


# Leaving in for debug
@router.get("/delete_gear_table",  response_class=HTMLResponse)
async def delete_gear_table():
    await drop_bg_items_table()


# Leaving in for debug
@router.get("/populate_modlist", response_description="item search",  response_class=HTMLResponse)
async def populate_mod_list():
    await populate_bg_mods()
    return HTMLResponse(status_code=200)
