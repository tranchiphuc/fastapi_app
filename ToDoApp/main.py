import os
from fastapi import FastAPI, Request

from .database import engine
from .models import Base
from .routers import auth, todos, admin, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

Base.metadata.create_all(bind=engine)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'templates'))
app.mount('/static', StaticFiles(directory=os.path.join(BASE_DIR, 'static')), name='static')
#app.mount('/static', StaticFiles(directory='ToDoApp/static'), name='static')

@app.get("/")
def get_home(req: Request):
    return templates.TemplateResponse(
    request=req,
    name='home.html',
    context={}
)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)