from abc import ABC, abstractmethod
import asyncio
from typing import List
from pydantic import BaseModel, ConfigDict
# from pydantic import BaseModel

from sqlalchemy import select
import yaml

from schemas.core import AIModel, AppConfigEntity, Consumer, FormSchema, ModelProviderEntity, ModelType
from database.models import Model, ModelProvider
from sqlalchemy.ext.asyncio import AsyncSession
from services.common_service import CommonService
from utils.utils import create_model_by_class, model_autofill
from langchain.schema import HumanMessage, BaseMessage
from langchain_core.language_models.base import BaseLanguageModel
from langchain.callbacks import AsyncIteratorCallbackHandler


class ModelProviderInstance(BaseModel, ABC):
    model_provider: ModelProvider

    model_config = ConfigDict(protected_namespaces=())
    
    def validate_provider_credentials(self) -> bool:
        """
        Validate provider credentials
        """
        raise NotImplementedError
    
    def model_types(self) -> List[ModelType]:
        raise NotImplementedError
    
    
    async def models(self) -> List[AIModel]:
        return CommonService.do_load_models_definition()[self.model_provider.name].models

    async def model_impl(self, model: Model, app_config: AppConfigEntity) -> BaseLanguageModel:
        raise NotImplementedError

    async def agenerate_task(self, model: Model, app_config: AppConfigEntity, messages: List[BaseMessage]):
        callback = AsyncIteratorCallbackHandler()
        model_impl: BaseLanguageModel = self.model_impl(model, app_config)
        task = asyncio.create_task(
            model_impl.agenerate(messages=[messages], callbacks=[callback])
        )
        return task, callback

        

    async def sync_models(self, model_provider: ModelProvider, consumer: Consumer, session: AsyncSession):
        ai_models: List[AIModel] = await self.models(model_provider)
        saved_models = (await session.execute(select(Model).where(Model.provider_id == model_provider.id))).scalars()
        if ai_models and len(ai_models) > 0:
            for ai_model in ai_models:
                if ai_model.id not in [db_model.name for db_model in saved_models]:
                    session.add(
                        create_model_by_class(
                            Model, 
                            consumer, 
                            provider_name = model_provider.name, 
                            provider_id = model_provider.id,
                            name = ai_model.id,
                            type = ai_model.support_types[0].value,
                            args = ai_model.args
                        )
                    )