from typing import Annotated
from pydantic import BaseModel, Field
from starlette.responses import RedirectResponse
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from ..dependencies import db_dependency
from ..models import Todos
from .auth import get_current_user


router = APIRouter(    
    prefix='/todos',
    tags=['todos'])

user_dependency = Annotated[dict, Depends(get_current_user)]
templates = Jinja2Templates(directory="TodoApp/templates")

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


### Pages ###

@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

        return templates.TemplateResponse(
            request, "todo.html", {"todos": todos, "user": user}
)
    except:
        return redirect_to_login()
    

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=50)
    priority: int = Field(ge=1, le=5)
    complete: bool

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user: user_dependency, db: db_dependency, todo_id: Annotated[int, Path(gt=0)], todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()
    return

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependency, db: db_dependency, todo_id: Annotated[int, Path(gt=0)]):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()
    return

@router.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()

@router.get("/", status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")