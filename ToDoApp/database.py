import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

import sqlalchemy
import psycopg2

import os
from os.path import join, dirname
import sys


dotenv_path = join(dirname(sys.argv[0]), '.env')
load_dotenv(dotenv_path)
dbname_pg = os.environ.get("POSTGRES_DB")
port_pg = os.environ.get("POSTGRES_PORT") 
user_pg = os.environ.get("POSTGRES_USER")
password_pg = os.environ.get("POSTGRES_PASSWORD")
host_pg = os.environ.get("POSTGRES_HOST")

#SQLALCHEMY_DATABASE_URL = f"postgresql://{user_pg}:{password_pg}@{host_pg}/{dbname_pg}"
SQLALCHEMY_DATABASE_URL ="postgresql://postgres:test1234@localhost/TodoApplicationDatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 
