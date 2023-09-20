from fastapi import  APIRouter, Depends
from pydantic import BaseModel
import sys 
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordRequestForm
from models import Users

 
 
try:
    import multipart
except ImportError:
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-multipart"])
    except subprocess.CalledProcessError as e:
        print("Error installing python-multipart:", e)
 
try:
    from passlib.context import CryptContext
except ImportError:
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "passlib"])
    except subprocess.CalledProcessError as e:
        print("Error installing passlib:", e)

from passlib.context import CryptContext

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



router = APIRouter()
bcrypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])

class CreateUserRequest(BaseModel):
    username: str
    email:str
    first_name : str
    last_name: str
    password: str
    role:str
    

def authenticate_user(username: str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True
    
    
@router.post("/auth", status_code=201)
async def create_user(db: db_dependency, 
                      create_user_request: CreateUserRequest):   
    # Create a new user instance
    create_user_model = Users( 
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()



@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed Authentification'
    return "Sucessful authentification"