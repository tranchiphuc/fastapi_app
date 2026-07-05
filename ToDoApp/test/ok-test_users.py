from fastapi import status

from ._utils import *
from ..dependencies import get_db
from ..routers.auth import get_current_user



app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_01_get_user_information(pytest_create_user):
    res = client.get("/user")
    assert res.status_code == status.HTTP_200_OK
    # print('\nTest_01-GET CURRENT USER: ', res.json())

def test_02_change_user_phone_number(pytest_create_user):
    res = client.put("/user/phone/0111222333")
    assert res.status_code == status.HTTP_204_NO_CONTENT

def test_change_user_password(pytest_create_user):
    json_data = {'password': 'Happy@111', 'new_password': '123'}
    res = client.put("/user/change_password", json=json_data)
    assert res.status_code == status.HTTP_204_NO_CONTENT

    

