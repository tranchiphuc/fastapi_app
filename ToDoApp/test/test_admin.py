from fastapi import status, HTTPException
from ._utils import *
from ..dependencies import get_db
from ..routers.auth import  get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.mark.asyncio
async def test_admin_read_all(pytest_create_user, pytest_create_todo):
    res = client.get("/user")
    assert res.status_code == status.HTTP_200_OK
    print('\nStep_01-GET CURRENT USER: ', res.json())


    res = client.get("/admin/todo")
    print('\nStep_02-GET ALL TODOS: ', res.json())
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [{**TODO_DICT, "id": 1}]

    todo_model = get_todo_by_id_from_db(1)
    assert compare_todo_object_and_dict(todo_model, TODO_DICT)
    