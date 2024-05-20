

from typing import List
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from database.models import Model, User
from schemas.core import ModelOut, UserOut

router = APIRouter()

@router.get("", response_model=Page[ModelOut])
async def models(db: AsyncSession = Depends(get_db)):
    return await paginate(db, select(Model))