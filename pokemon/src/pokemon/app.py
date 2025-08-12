import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from pokemon.routes import router

app = FastAPI()

app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# TODO: This is codesmell -- makes sure that able to url_for("root") for htmx methods
app.mount("/", StaticFiles(directory="static"), name="root")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=4002, reload=True)
