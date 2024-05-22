

from typing import List
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from database.models import Model, ModelProvider, User
from schemas.core import ModelOut, ModelProviderIn, ModelProviderOut, UserOut
from services.model_service import ModelService
from fastapi.exceptions import HTTPException
from loguru import logger
from utils.deps import get_consumer
from utils.utils import model_autofill

router = APIRouter()

@router.get("/models", response_model=Page[ModelOut])
async def models(db: AsyncSession = Depends(get_db)):
    return await paginate(db, select(Model))


@router.post("/providers/{provider_id}/models", response_model=List[ModelOut])
async def sync_models_by_provider(provider_id: str,  db: AsyncSession = Depends(get_db)):
    model_provider: ModelProvider = await db.get(ModelProvider, provider_id)
    if not model_provider:
        raise HTTPException(status_code=404)
    await ModelService.sync_models_by_provider(model_provider)
    return providers(provider_id, db)

@router.get("/providers/{provider_id}/models", response_model=List[ModelOut])
async def providers(provider_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model).where(Model.provider_id == provider_id))
    return result.fetchall()

@router.post("/providers", response_model=ModelProviderOut)
async def providers(model_provider_in: ModelProviderIn, db: AsyncSession = Depends(get_db), consumer = Depends(get_consumer)):
    logger.info("model_provider_in: {}", model_provider_in.model_dump())
    provider = ModelProvider(name="123")
    provider.name = "123"
    model_autofill(provider, consumer)
    db.add(provider)
    return db.get(ModelProvider, provider.id)