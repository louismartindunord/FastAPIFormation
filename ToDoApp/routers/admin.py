from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, FastAPI, Depends, HTTPException, Path, dependencies
from models import Todos
from database import engine, SessionLocal
from pydantic import BaseModel, Field

from routers import todos
from .auth import get_current_user




router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()
        

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todo", status_code=200)
async def read_all(user : user_dependency, db:db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentification failed")
  
    return db.query(Todos).all()