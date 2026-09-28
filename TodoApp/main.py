
from fastapi import FastAPI, Request
from .models import Base
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .database import engine
from .routers import auth, todos, admin, users
app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="TodoApp/templates")

app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

@app.get("/")
def test(request: Request):
    return templates.TemplateResponse(   request=request,
    name="home.html",
    context={"request": request})

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)