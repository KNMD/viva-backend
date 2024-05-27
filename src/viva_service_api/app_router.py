

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from schemas.core import AppEntity, AppEntityPatch, CategoryEntity, CommonResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from services.common_service import CommonService
from database.models import App
from utils.deps import get_consumer
from utils.utils import model_autofill

router = APIRouter(
    default_response_class=CommonResponse,
    prefix="/apps"
)

@router.get("", response_model=Page[AppEntity])
async def page(db: AsyncSession = Depends(get_db)):
    return await paginate(db, select(App))

@router.get("/{id}", response_model=Optional[AppEntity])
async def page(id: str, db: AsyncSession = Depends(get_db)):
    return await db.get(App, id)

@router.post("", response_model=AppEntity)
async def save(entity: AppEntity, db: AsyncSession = Depends(get_db),  consumer = Depends(get_consumer)):
    model: App = App(
        **entity.model_dump()
    )
    model_autofill(model, consumer, status = 0)
    db.add(model)
    return await db.get(App, model.id)

@router.put("/{id}", response_model=AppEntity)
async def update(id: str, entity: AppEntity, db: AsyncSession = Depends(get_db),  consumer = Depends(get_consumer)):
    model: App = await db.get(App, id)
    if not model:
        raise HTTPException(status_code=404)
    for key, value in entity.model_dump(exclude=["id", "status"]).items():
        setattr(model, key, value)
    model_autofill(model, consumer)
    return await db.get(App, id)

@router.patch("/{id}", response_model=AppEntity)
async def patch(id: str, entity: AppEntityPatch, db: AsyncSession = Depends(get_db),  consumer = Depends(get_consumer)):
    model: App = await db.get(App, id)
    if not model:
        raise HTTPException(status_code=404)
    for key, value in entity.model_dump(exclude=["id"]).items():
        if value is not None:
            setattr(model, key, value)     
        
    model_autofill(model, consumer)
    return await db.get(App, id)

@router.delete("/{id}", response_model=AppEntity)
async def delete(id: str, db: AsyncSession = Depends(get_db)):
    model: App = await db.get(App, id)
    if not model:
        raise HTTPException(status_code=404)
    await db.delete(model)
    return model



