import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_URL")


engine = None
SessionLocal = None
if SQLALCHEMY_DATABASE_URL != None:
  engine = create_engine(
      SQLALCHEMY_DATABASE_URL,
      echo=True
  )
  SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()