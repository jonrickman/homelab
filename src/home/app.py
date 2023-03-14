from fastapi import FastAPI, Depends, Request, Form, status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

templates=Jinja2Templates(directory="templates")
app = FastAPI()


def get_db():
    db = SessionLocal()
    try: 
        yield db
    except Exception as e:
        # TODO: Setup logging
        print(e)
    finally:
        db.close()

@app.get("/")
def home():
    return templates.TemplateResponse("index.html")

#region YouTube
VIDEOS="/videos/"
@app.get(VIDEOS)
def videos_home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html")

@app.get(VIDEOS)
def videos_add(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html")

@app.get(VIDEOS+"/search")
def videos_home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html")
#endregion
