from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, dependencies
import models
from models import Todos
from database import engine, SessionLocal
from pydantic import BaseModel, Field
import sqlalchemy
import psycopg2
from routers import auth, todos,  admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
