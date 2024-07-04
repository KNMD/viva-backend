

import datetime
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from database.models import Model, ModelProvider, User
from schemas.core import CommonResponse, FormSchema, ModelDefinitioin, ModelInt, ModelEntity, ModelProviderEntity, ModelProviderIn
from services.model_service import ModelService
from fastapi.exceptions import HTTPException
from loguru import logger
from exceptions.exception import ResponseException
from services.common_service import CommonService
from services.model_provider.base import ModelProviderInstance
from services.model_provider.openai import OpenAIModelProviderInstance
from services.model_provider.mapper import model_provider_mapper
from utils.deps import get_consumer
from utils.utils import create_model_by_class, model_autofill
from config.settings import app_settings
from collections import defaultdict

router = APIRouter(
    prefix="/models",
    default_response_class=CommonResponse
)

@router.get("", response_model=Page[ModelEntity])
async def models(db: AsyncSession = Depends(get_db)):
    return await paginate(db, select(Model))

@router.get("/groups")
async def models(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model))
    models = result.scalars().fetchall()
    grouped = defaultdict(list)
    for item in models:
        grouped[item.provider_name].append(item)
    result = [{"providerName": key, "modelList": (await load_model_def_merge_args(key, value))} for key, value in grouped.items()]
    return result



@router.get("/{id}", response_model=Optional[ModelEntity])
async def models(id: str, db: AsyncSession = Depends(get_db)):
    return await db.get(Model, id)
    

@router.get("/providers/{provider_id}/models", response_model=List[ModelEntity])
async def providers(provider_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model).where(Model.provider_id == provider_id))
    return result.fetchall()

@router.get("/providers/{provider_id}/models/{model_id}", response_model=List[ModelEntity])
async def providers(provider_id: str, model_id: str, db: AsyncSession = Depends(get_db)):
    return await db.get(Model, model_id)

@router.delete("/providers/{provider_id}/models/{model_id}", response_model=ModelEntity)
async def providers(provider_id: str, model_id: str, db: AsyncSession = Depends(get_db)):
    model = await db.get(Model, model_id)
    if model:
        await db.delete(model)
    else:
        raise HTTPException(status_code=404)
    return model

@router.post("/providers/{provider_id}/models", response_model=ModelEntity)
async def providers(provider_id: str, model_in: ModelInt, db: AsyncSession = Depends(get_db), consumer = Depends(get_consumer)):
    provider = await db.get(ModelProvider, provider_id)
    if not provider:
        raise HTTPException(status_code=404)
    
    model = Model(**model_in.model_dump(exclude="type"), provider_id = provider.id, provider_name = provider.name, type = str(model_in.type.value))
    model_autofill(model, consumer)
    db.add(model)
    return await db.get(Model, model.id)

async def load_model_def_merge_args(provider_name, models: List[Model]) -> List[ModelEntity]:
    model_def: ModelDefinitioin = (await CommonService.do_load_models_definition())[provider_name]
    display_args = model_def.display_args['default']
    model_entities = []
    for model in models:
        model_entity = ModelEntity.model_validate(model)
        model_entity.display_args = display_args
        for ai_model in model_def.models:
            if model.name == ai_model.id:
                if ai_model.display_args is not None:
                    model_entity.display_args = display_args_merge(display_args, ai_model.display_args)
                model_entities.append(model_entity)
    
    return model_entities
        
def display_args_merge(default_args: List[FormSchema], section_args: List[Dict[str, Any]]) -> List[FormSchema]:
    new_args = []
    for arg in default_args:
        form_dict = arg.model_dump()
        for dict_arg in section_args:
            if dict_arg['variable'] == arg.variable:
                merge_dict = {**form_dict, **dict_arg}
                form_schema = FormSchema.model_validate(merge_dict)
                new_args.append(form_schema)
            else:
                new_args.append(arg)




    

@router.post("/providers", response_model=ModelProviderEntity)
async def providers(model_provider_in: ModelProviderIn, db: AsyncSession = Depends(get_db), consumer = Depends(get_consumer)):
    
    provider:ModelProvider = create_model_by_class(
        ModelProvider, 
        consumer, 
        **model_provider_in.model_dump(exclude="support_model_sync"),
        class_name = model_provider_in.name
    )
    provider.created_at = datetime.datetime.now()
    
    model_provider_instance: ModelProviderInstance = model_provider_mapper[model_provider_in.name](
        model_provider = ModelProviderEntity.model_validate(provider)
    )
    try: 
        if not (await model_provider_instance.validate_provider_credentials()):
            raise ResponseException.err(error_var="model_provider_auth_fail", status = 400)
        models_def = await CommonService.do_load_models_definition().get(provider.name, None)
        if models_def:
            await model_provider_instance.sync_models(consumer, db)

    except NotImplementedError as e:
        logger.info("class name: {} not implemented. error: {}", provider.class_name, e)
    db.add(provider)
    return await db.get(ModelProvider, provider.id)