from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import db_dependency
from ..models import Users
from .auth import get_current_user, pwd_context

router = APIRouter(prefix='/user', tags=['user'])
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=3)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_information(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Authentication Failed")
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not pwd_context.verify(user_verification.password, user_model.hashed_password):
    # if user_verification.password != user_model.hashed_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is not correct")
    user_model.hashed_password = pwd_context.hash(user_verification.new_password)
    # user_model.hashed_password = user_verification.new_password
    db.add(user_model)
    db.commit()
    return user_model

@router.put("/phone/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
    return