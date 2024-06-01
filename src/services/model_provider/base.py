from abc import ABC, abstractmethod
from typing import List

from sqlalchemy import select

from schemas.core import AIModel, Consumer, FormSchema, ModelProviderEntity, ModelType
from database.models import Model, ModelProvider
from sqlalchemy.ext.asyncio import AsyncSession

from utils.utils import model_autofill

class ModelProviderInstance(ABC):
        
    
    def validate_provider_credentials(self, model_provider: ModelProvider) -> bool:
        """
        Validate provider credentials
        """
        raise NotImplementedError
    
    def model_types(self) -> List[ModelType]:
        raise NotImplementedError
    
    
    async def models(self, model_provider: ModelProvider) -> List[AIModel]:
        """
        get provider all models
        """
        raise NotImplementedError


    async def sync_models(self, model_provider: ModelProvider, consumer: Consumer, session: AsyncSession):
        ai_models: List[AIModel] = self.models()
        saved_models = (await session.execute(select(Model).where(Model.provider_id == model_provider.id))).scalars()
        if ai_models and len(ai_models) > 0:
            for ai_model in ai_models:
                if ai_model.name in (db_model.name for db_model in saved_models):
                    session.add(
                        model_autofill(
                            Model(
                                provider_name = model_provider.name, 
                                provider_id = model_provider.id,
                                **ai_model.model_dump() 
                            ),
                            consumer
                        )
                    )