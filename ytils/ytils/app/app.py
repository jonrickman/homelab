from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import app.routers as routers
from .settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount('/static', StaticFiles(directory=settings.static_files), name="static")

app.include_router(routers.generic_router)
app.include_router(routers.api_key_router)
app.include_router(routers.video_router)
