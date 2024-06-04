from abc import ABC, abstractmethod
from typing import List

from sqlalchemy import select
import yaml

from schemas.core import AIModel, Consumer, FormSchema, ModelProviderEntity, ModelType
from database.models import Model, ModelProvider
from sqlalchemy.ext.asyncio import AsyncSession
from services.common_service import CommonService
from utils.utils import create_model_by_class, model_autofill




class ModelProviderInstance(ABC):
    
    
    def validate_provider_credentials(self, model_provider: ModelProvider) -> bool:
        """
        Validate provider credentials
        """
        raise NotImplementedError
    
    def model_types(self) -> List[ModelType]:
        raise NotImplementedError
    
    
    async def models(self, model_provider: ModelProvider) -> List[AIModel]:
        return CommonService.do_load_models_definition()[model_provider.name]



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
                            type = ai_model.supportTypes[0].value,
                            args = ai_model.args
                        )
                    )