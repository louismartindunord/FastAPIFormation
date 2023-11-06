from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, FastAPI, Depends, HTTPException, Path, dependencies
from models import Todos
from database import engine, SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user
from models import Users

from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["sha256_crypt", "des_crypt"], deprecated='auto')

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()
        

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)



@router.get('/')
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/password")
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    
@router.put("/phone_number/{phone_number}", status_code=203)
async def change_phone_number(db: db_dependency, user: user_dependency, phone_number:str):
    if user is None: 
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()