from fastapi import APIRouter
from starlette import status
from pydantic import BaseModel
from pwdlib import PasswordHash
from ..models import Users
from ..dependencies import db_dependency

router = APIRouter(prefix='/users', tags=['users'])
pwd_context = PasswordHash.recommended()


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        is_active = True,
        hashed_password = pwd_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()
    return create_user_model


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency):
    users = db.query(Users).all()
    return users

