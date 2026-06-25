from typing import Annotated
from starlette import status

from fastapi import APIRouter, Depends, HTTPException, Path
from ..dependencies import db_dependency
from ..models import Users
from .auth import get_current_user, pwd_context, SECRET_KEY, ALGORITHM

router = APIRouter(prefix='/users', tags=['users'])
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_information(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_password(user: user_dependency, db: db_dependency, password: str, new_password: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not pwd_context.verify(password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is not correct")
    user_model.hashed_password = pwd_context.hash(new_password)
    db.add(user_model)
    db.commit()
    return