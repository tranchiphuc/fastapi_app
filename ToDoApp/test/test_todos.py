from fastapi import status
from ..models import Todos, Users
from ..dependencies import get_db
from ..routers.auth import get_current_user
from ._utils import *


app.dependency_overrides[get_db] = override_get_db
# app.dependency_overrides[get_current_user] = override_get_current_user

# print('SQLALCHEMY_DATABASE_URL = ', SQLALCHEMY_DATABASE_URL)
def test_read_all(create_todo, create_user):
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [{**TODO_DICT, "id": 1}]
