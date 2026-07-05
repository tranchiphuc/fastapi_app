from fastapi import status
from ..dependencies import get_db
from ..routers.auth import get_current_user
from ._utils import *

         
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

    

def test_01_read_all(pytest_create_todo):
    res = client.get("/")
    #print("\nRESPONSE: ", res.json(), "\n")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [{**TODO_DICT, "id": 1}]

def test_05_create_todo(pytest_create_todo):
    res = client.post("/todo", json=TODO_DICT_NEW)
    assert res.status_code == status.HTTP_201_CREATED
    res = client.get("/")
    $print("\nRESPONSE: ", res.json(), "\n")
    todo_model = get_todo_by_id_from_db(2)
    assert compare_todo_object_and_dict(todo_model, TODO_DICT_NEW)

  
def test_02_read_todo_by_id(pytest_create_todo):
    res = client.get("/todo/1")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {**TODO_DICT, "id": 1}


def test_03_delete_todo(pytest_create_todo):
    res = client.delete("/todo/1")
    assert res.status_code == status.HTTP_204_NO_CONTENT
    todo_model = get_todo_by_id_from_db(1)
    assert todo_model is None

def test_04_delete_todo_not_found(pytest_create_todo):
    res = client.delete("/todo/111")
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_06_update_todo(pytest_create_todo):
    res = client.put("/todo/1", json=TODO_DICT_UPDATE)
    assert res.status_code == status.HTTP_204_NO_CONTENT
    todo_model = get_todo_by_id_from_db(1)
    assert compare_todo_object_and_dict(todo_model, TODO_DICT_UPDATE)

def test_07_update_todo_not_exist(pytest_create_todo):
    res = client.put("/todo/111", json=TODO_DICT_NEW)
    assert res.status_code == status.HTTP_404_NOT_FOUND


