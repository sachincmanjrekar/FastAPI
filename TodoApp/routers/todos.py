from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from ..models import Todo
from ..database import engine, SessionLocal
from starlette import status
from .auth import get_current_user
router = APIRouter(
    prefix="/master_todos",
    tags=["master_todos"],
)
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="TodoApp/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=200)
    priority: int = Field(default=1)
    complete: bool

def redirect_to_login():

    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response
### Pages ###



@router.get("/todo-page")
async def render_todo_page(request: Request, db:db_dependency):

    try:
        user = await get_current_user(request)
        if user is None:
            return redirect_to_login()

        todos = db.query(Todo).filter(Todo.owner_id==user.get("user_id")).all()
        return templates.TemplateResponse("todos.html", {"request": request, "todos": todos, "user": user})

    except Exception as e:
        return redirect_to_login()


### ENDPOINTS ###
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="User not found.")
    return db.query(Todo).filter(Todo.owner_id == user.get('user_id')).all()

@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user:user_dependency, db:db_dependency, todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not found.")
    todo_model = (db.query(Todo).filter(Todo.id == todo_id)\
                  .filter(Todo.owner_id==user.get("user_id")).first())
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo Not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency, db: db_dependency, todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="User not found.")
    print(todo_request)
    print(user)
    new_todo_row = Todo(**todo_request.dict(), owner_id=user.get('user_id'))
    db.add(new_todo_row)
    db.commit()


@router.put("/todo/update/{existing_todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_dependency, db: db_dependency, to_update_todo_row_values:TodoRequest, existing_todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not found.")
    existing_todo_row = db.query(Todo).filter(Todo.id == existing_todo_id).filter(Todo.owner_id==user.get("user_id")).first()
    if existing_todo_row is None:
        raise HTTPException(status_code=404, detail='Row not found with todo_id')
    existing_todo_row.title = to_update_todo_row_values.title
    existing_todo_row.description = to_update_todo_row_values.description
    existing_todo_row.priority = to_update_todo_row_values.priority
    existing_todo_row.complete = to_update_todo_row_values.complete

    db.add(existing_todo_row)
    db.commit()


@router.delete("/todo/delete/{existing_todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db:db_dependency,existing_todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not found.")
    existing_todo_row = db.query(Todo).filter(Todo.id == existing_todo_id).filter(Todo.owner_id==user.get("user_id")).first()
    if existing_todo_row is None:
        raise HTTPException(status_code=404, detail='Row not found with todo_id')

    db.query(Todo).filter(Todo.id == existing_todo_id).delete()
    db.commit()