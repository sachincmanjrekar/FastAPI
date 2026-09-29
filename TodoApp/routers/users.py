from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from ..database import SessionLocal
from ..models import Users
from .auth import get_current_user

router = APIRouter(    prefix="/Users",
    tags=["USERAPIS"],)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/current_user_info", status_code=status.HTTP_200_OK)
async def get_user(db:db_dependency, user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return db.query(Users).filter(Users.id == user.get("user_id")).first()

@router.put("/update_current_user_password/", status_code=status.HTTP_204_NO_CONTENT)
async def update_current_user_password(db:db_dependency, user:user_dependency,
                   password: str= Body(...),
                   new_password:str= Body(...)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    user_row =  db.query(Users).filter(Users.id == user.get("user_id")).first()

    if not bcrypt_context.verify(password, user_row.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    user_row.hashed_password = bcrypt_context.hash(new_password)

    db.add(user_row)
    db.commit()

@router.put("/update_phone_number/", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(db:db_dependency, user:user_dependency, new_phone_number:str= Body(..., embed=True)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    user_row =  db.query(Users).filter(Users.id == user.get("user_id")).first()
    user_row.phone_number = new_phone_number
    db.add(user_row)
    db.commit()

