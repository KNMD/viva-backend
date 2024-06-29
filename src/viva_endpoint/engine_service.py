

import importlib
from typing import Any, Dict, List
from loguru import logger
from schemas.core import AppConfigEntity, AppEntity, AppInput, Consumer, Message, ModelEntity, ModelProviderEntity
from database.database import open_session
from database.models import Model, ModelProvider
from services.model_provider.base import ModelProviderInstance
from config.settings import app_settings
from services.model_provider.mapper import model_provider_mapper
from services.memory.memory_providers import RedisMessageMemory

class EngineService():

    @classmethod
    async def output(cls, input: AppInput, app: AppEntity, consumer: Consumer):

        model = await cls.get_model_by_id(app.app_config.base_model_id)
        model_provider = await cls.get_model_provider(model.provider_id)
        messages: List[Message] = input.messages
        messages = await cls._variable_resolve(messages, input.variable_vals)
        message_memory = None
        if input.conversation_id:
            message_memory = RedisMessageMemory(
                app = app,
                model = model,
                model_provider = model_provider,
                conversation_id = input.conversation_id, 
                redis_url=app_settings.redis_url, 
                consumer=consumer,
                ttl = input.conversation_ttl if input.conversation_ttl is not None else app_settings.redis_default_ttl
            )
            memory_messages = await message_memory.retrieval()
            if memory_messages:
                messages = memory_messages + messages
            
        model_provider_instance: ModelProviderInstance = model_provider_mapper[model.provider_name](model_provider = model_provider, memory = message_memory)

        return model_provider_instance.agenerate(model, app.app_config, messages=messages)

    async def _variable_resolve(messages: List[Message], variables: Dict[str, Any]) -> List[Message]:
        new_messages = []
        for message in messages:
            resolve_prompt_message = message
            if variables is not None:
                for key, val in variables.items():
                    resolve_prompt_message = message.replace("{{" + key + "}}", val)
            new_messages.append(resolve_prompt_message)

        return new_messages
        
    @classmethod
    async def get_model_provider(cls, provider_id) -> ModelProviderEntity:
        async with open_session() as session:
            model_provider: ModelProvider = await session.get(ModelProvider, provider_id)
            return ModelProviderEntity.model_validate(model_provider)
        
    @classmethod
    async def get_model_by_id(cls, model_id) -> ModelEntity:
        async with open_session() as session:
            model: Model = await session.get(Model, model_id)
            return ModelEntity.model_validate(model)

