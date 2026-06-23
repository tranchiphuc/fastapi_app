from fastapi import APIRouter
from starlette import status
from pydantic import BaseModel
from ..models import Users


router = APIRouter(prefix='/users', tags=['users'])

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/")
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        is_active = True,
        hashed_password = create_user_request.password
    )
    return create_user_model


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user():
    return {'user': 'Test user'}

