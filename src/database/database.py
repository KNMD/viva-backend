import os
from typing import Iterator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_URL")
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:123456@dev-host:5432/postgres"


engine = None
SessionLocal = None
if SQLALCHEMY_DATABASE_URL != None:
  engine = create_async_engine(
      SQLALCHEMY_DATABASE_URL,
      echo=True
  )
  SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


async def get_db() -> Iterator[AsyncSession]: # type: ignore
    db = AsyncSession(engine)
    async with db.begin():
        yield db
