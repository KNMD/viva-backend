

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from schemas.core import AppEntity, CategoryEntity, CommonResponse, DatasetEntity
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from database.models import Dataset
from utils.deps import get_consumer
from utils.utils import model_autofill

router = APIRouter(
    default_response_class=CommonResponse,
    prefix="/dataset"
)

@router.get("", response_model=Page[DatasetEntity])
async def page(db: AsyncSession = Depends(get_db)):
    return await paginate(db, select(Dataset))

@router.get("/{id}", response_model=DatasetEntity)
async def page(id: str, db: AsyncSession = Depends(get_db)):
    return await db.get(Dataset, id)

@router.post("", response_model=DatasetEntity)
async def save(entity: CategoryEntity, db: AsyncSession = Depends(get_db), consumer = Depends(get_consumer)):
    model = Dataset(
        **entity.model_dump()
    )
    model_autofill(model, consumer)
    await db.add(model)
    return await db.get(Dataset, id)

@router.put("/{id}", response_model=DatasetEntity)
async def update(id: str, entity: CategoryEntity, db: AsyncSession = Depends(get_db), consumer = Depends(get_consumer)):
    model = await db.get(Dataset, id)
    if not model:
        raise HTTPException(status_code=404)
    for key, value in entity.model_dump(exclude="id").items():
        setattr(model, key, value)
    model_autofill(model, consumer)
    return await db.get(Dataset, id)

@router.delete("/{id}")
async def delete(id: str, db: AsyncSession = Depends(get_db)):
    model = await db.get(Dataset, id)
    if not model:
        raise HTTPException(status_code=404)
    db.delete(model)



