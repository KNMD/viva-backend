

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy import select

from schemas.core import CategoryEntity, CommonResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from database.models import Category
from services.common_service import CommonService
from utils.deps import get_consumer
from utils.utils import model_autofill

router = APIRouter(
    default_response_class=CommonResponse,
    prefix="/categories"
)

@router.get("", response_model=Page[CategoryEntity])
async def page(db: AsyncSession = Depends(get_db)):
    return await paginate(db, select(Category))

@router.get("/{id}", response_model=CategoryEntity)
async def page(id: str, db: AsyncSession = Depends(get_db)):
    return await db.get(Category, id)

@router.post("", response_model=CategoryEntity)
async def save(entity: CategoryEntity, db: AsyncSession = Depends(get_db),  consumer = Depends(get_consumer)):
    model: Category = Category(
        **entity.model_dump(),
        id = await CommonService.category_hierarchy(entity.parent_id)
    )
    model_autofill(model, consumer)
    await db.add(model)
    return await db.get(Category, id)

@router.put("/{id}", response_model=CategoryEntity)
async def update(id: str, entity: CategoryEntity, db: AsyncSession = Depends(get_db),  consumer = Depends(get_consumer)):
    model: Category = await db.get(Category, id)
    if not model:
        raise HTTPException(status_code=404)
    for key, value in entity.model_dump(exclude="id").items():
        setattr(model, key, value)
    model_autofill(model, consumer)
    return await db.get(Category, id)

@router.delete("/{id}")
async def delete(id: str, db: AsyncSession = Depends(get_db)):
    model: Category = await db.get(Category, id)
    if not model:
        raise HTTPException(status_code=404)
    db.delete(model)



