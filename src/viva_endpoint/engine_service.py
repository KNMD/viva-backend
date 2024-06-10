

from schemas.core import AppConfigEntity, AppInput, Consumer
from database.database import open_session
from database.models import Model, ModelProvider
from services.model_provider.base import ModelProviderInstance
from config.settings import app_settings


class EngineService():

    @classmethod
    async def output(cls, input: AppInput, app_config: AppConfigEntity, consumer: Consumer):

        model: Model = await cls.get_model_by_id(app_config.base_model_id)
        model_provider = await cls.get_model_provider(model.provider_id)
        model_provider_instance: ModelProviderInstance = eval(app_settings.model_provider_mapper[model.provider_name])(model_provider)

        return model_provider_instance.agenerate_task(model, app_config, messages=input.messages)

        
        
        

    @classmethod
    async def get_model_provider(cls, provider_id) -> ModelProvider:
        async with open_session() as session:
            model_provider: ModelProvider = await session.get(ModelProvider, provider_id)
            return model_provider
        
    @classmethod
    async def get_model_by_id(cls, model_id) -> Model:
        async with open_session() as session:
            model: Model = await session.get(Model, model_id)
            return model

