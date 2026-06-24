from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status

from fastapi import APIRouter, Depends, HTTPException, Path
from ..dependencies import db_dependency
from ..models import Todos
from .auth import get_current_user


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=50)
    priority: int = Field(ge=1, le=5)
    complete: bool

router = APIRouter()
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def put_todo(db: db_dependency, todo_id: Annotated[int, Path(gt=0)], todo_request: TodoRequest):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
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
def delete_todo(db: db_dependency, todo_id: Annotated[int, Path(gt=0)]):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()
    return

@router.post("/todo", status_code=status.HTTP_201_CREATED)
def post_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()

@router.get("/", status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")