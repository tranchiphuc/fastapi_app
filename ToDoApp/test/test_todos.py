from _pytest import deprecated
from ToDoApp.test._utils import TestingSessionLocal
from _pytest import fixtures
from _pytest import fixtures
from fastapi import status
from ..models import Todos, Users
from ..dependencies import get_db
from ..routers.auth import get_current_user
from ._utils import *

         
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def get_todo_by_id_from_db(id):
    db = TestingSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id==id).first()
    return todo_model

def check_todo_object_and_dict(todo_obj, todo_dict):
    if todo_obj.title != todo_dict.get("title"):
        return False
    if todo_obj.description != todo_dict.get("description"):
        return False    
    if todo_obj.priority != todo_dict.get("priority"):
        return False
    if todo_obj.complete != todo_dict.get("complete"):
        return False
    return True
    

# print('SQLALCHEMY_DATABASE_URL = ', SQLALCHEMY_DATABASE_URL)
def test_read_all(pytest_create_todo):
    res = client.get("/")
    # res = client.get("/", headers={"Authorization": f"Bearer {TOKEN}"})
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [{**TODO_DICT, "id": 1}]

def test_read_todo_by_id(pytest_create_todo):
    res = client.get("/todo/1")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {**TODO_DICT, "id": 1}

def test_delete_todo(pytest_create_todo):
    res = client.delete("/todo/1")
    assert res.status_code == status.HTTP_204_NO_CONTENT
    todo_model = get_todo_by_id_from_db(1)
    assert todo_model is None

def test_delete_todo_not_found(pytest_create_todo):
    res = client.delete("/todo/111")
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_create_todo():
    res = client.post("/todo", json=TODO_DICT)
    assert res.status_code == status.HTTP_201_CREATED
    todo_model = get_todo_by_id_from_db(1)
    assert check_todo_object_and_dict(todo_model, TODO_DICT)

def test_update_todo():
    res = client.put("/todo/1", json=TODO_DICT_NEW)
    assert res.status_code = status.HTTP_204_NO_CONTENT
    todo_model = get_todo_by_id_from_db(1)
    assert check_todo_object_and_dict(todo_model, TODO_DICT_NEW)
