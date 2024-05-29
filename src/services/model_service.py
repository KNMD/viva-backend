

from typing import List
from database.models import Model, ModelProvider
from services.model_provider.base import ModelProviderInstance
from schemas.core import AIModel, Consumer
from utils.utils import model_autofill
from sqlalchemy.ext.asyncio import AsyncSession



class ModelService():

    @classmethod
    def create_model_provider_instance(model_provider: ModelProvider) -> ModelProviderInstance:
        provider_instance_class = type(model_provider.class_name, (ModelProviderInstance,), {})
        return provider_instance_class()

    @classmethod
    async def sync_models_by_provider(cls, model_provider: ModelProvider, saved_models: Model, consumer: Consumer, session: AsyncSession):

        model_provider_instance: ModelProviderInstance = cls.create_model_provider_instance(model_provider)
        
        valid = model_provider_instance.validate_provider_credentials(model_provider.credential_config)
        if valid:
            ai_models: List[AIModel] = model_provider_instance.models()
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

    
