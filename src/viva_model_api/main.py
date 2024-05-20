from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, List
from typing import Any, Iterator
import uuid

import uvicorn
from faker import Faker
from fastapi import Depends, FastAPI
from pydantic import UUID4, BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

from fastapi_pagination import LimitOffsetPage, Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from database.models import User
from schemas.core import UserIn, UserOut

faker = Faker()

engine = create_async_engine("postgresql+asyncpg://postgres:123456@localhost:5432/postgres", echo=True)








async def get_db() -> Iterator[AsyncSession]: # type: ignore
    db = AsyncSession(engine)
    async with db.begin():
        yield db

app = FastAPI()
add_pagination(app)


@app.post("/users")
async def create_user(user_in: UserIn, db: AsyncSession = Depends(get_db)) -> UserOut:
    random_uuid = uuid.uuid4()
    print(random_uuid)
    user = User(name=user_in.name, email=user_in.email, id=random_uuid)
    db.add(user)
    await db.commit()

    return UserOut.from_orm(user)


@app.get("/users/default")
async def get_users(db: AsyncSession = Depends(get_db)) -> Page[User]:
    return await paginate(db, select(User))


if __name__ == "__main__":
    uvicorn.run("test:app")