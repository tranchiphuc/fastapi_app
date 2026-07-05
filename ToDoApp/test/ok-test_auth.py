from fastapi import status, HTTPException
import jwt
from ._utils import *
from ..dependencies import get_db
from ..routers.auth import authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user


app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(pytest_create_user):
    db = TestingSessionLocal()

    authen_user = authenticate_user(pytest_create_user.username, 'Happy@111', db)
    assert authen_user is not None

    with pytest.raises(HTTPException) as exc_info:
        authenticate_user('aaaaa', '123', db)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_access_token():
    token = create_access_token(USER_DICT.get('username'), 
                                USER_DICT.get('id'),
                                USER_DICT.get('role'),
                                timedelta(days=1))
    
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get('sub')
        user_id = payload.get('id')
        role = payload.get('role')

        assert username == USER_DICT.get('username')
        assert user_id == USER_DICT.get('id')
        assert role == USER_DICT.get('role')
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid or expired")


@pytest.mark.asyncio
async def test_get_current_user(pytest_create_user):
    token = create_access_token(
    USER_DICT.get('username'), 
    USER_DICT.get('id'), 
    USER_DICT.get('role'), 
    timedelta(days=1)
    )

    payload = await get_current_user(token)
    # print('\nDebug: Payload = ', payload)
    username = payload.get('username')
    user_id = payload.get('id')
    role = payload.get('role')

    # print('\nDebug: USER_DICT = ', USER_DICT)
    assert username == USER_DICT.get('username')
    assert user_id == USER_DICT.get('id')
    assert role == USER_DICT.get('role')   

