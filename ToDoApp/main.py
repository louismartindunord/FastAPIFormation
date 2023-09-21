from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, dependencies
import models
from models import Todos
from database import engine, SessionLocal
from pydantic import BaseModel, Field

from routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(todos.router)