from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import find_dotenv, load_dotenv
from fastapi import Request
from sqlalchemy import create_engine
from typing import Generator
import os

load_dotenv(find_dotenv())

# SQLACHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:postgres@localhost:5432/lmi'
SQLACHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(SQLACHEMY_DATABASE_URL, pool_pre_ping=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db(request: Request) -> Generator:
  return request.state.db