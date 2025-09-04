from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from app.depends import templates
from app.crud import api_key


PREFIX = "/api_keys"

router = APIRouter(prefix=PREFIX)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):

    api_keys = await api_key.find()
    context = {
        "request": request,
        "api_keys": api_keys
    }

    return templates.TemplateResponse("api_keys.html.j2", context=context)


@router.post("/create")
async def create_model(key_value: str = Form(...)):
    payload = {
        "key": key_value
    }
    await api_key.create(**payload)

    return RedirectResponse("/api_keys", status_code=303)
