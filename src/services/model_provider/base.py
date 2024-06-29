from abc import ABC, abstractmethod
import asyncio
from typing import AsyncIterable, List, Optional
from loguru import logger
from pydantic import BaseModel, ConfigDict
# from pydantic import BaseModel

from sqlalchemy import select
import yaml

from schemas.core import AIModel, AppCompletionChunk, AppConfigEntity, Consumer, FormSchema, Message, ModelProviderEntity, ModelType
from database.models import Model, ModelProvider
from sqlalchemy.ext.asyncio import AsyncSession
from services.common_service import CommonService
from services.memory.base import BaseMessageMemory
from utils.utils import create_model_by_class, model_autofill
from langchain.schema import HumanMessage, BaseMessage
from langchain_core.language_models.base import BaseLanguageModel
from langchain.callbacks import AsyncIteratorCallbackHandler
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai._streaming import AsyncStream

class ModelProviderInstance(BaseModel, ABC):
    model_provider: Optional[ModelProviderEntity] = None
    memory: Optional[BaseMessageMemory] = None
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

    async def _agenerate(self, model: Model, app_config: AppConfigEntity, messages: List[Message]) ->  ChatCompletion | AsyncStream[ChatCompletionChunk]:
        raise NotImplementedError
    
    async def agenerate(self, model: Model, app_config: AppConfigEntity, messages: List[Message]) -> AsyncIterable[AppCompletionChunk]:
        generate_output =  await self._agenerate(model, app_config, messages)
        sentence = ""
        async for chunk in generate_output:
            app_chunk = AppCompletionChunk.model_validate(chunk.to_dict())
            app_chunk.model = model.id
            if chunk.choices[0].delta.content:
                sentence += chunk.choices[0].delta.content
            yield app_chunk
        if self.memory:
            new_messages = [messages[len(messages) - 1], Message(
                role = "assistant",
                content = sentence
            )]
            await self.memory.append(new_messages)
        
        
        



        

    async def sync_models(self, consumer: Consumer, session: AsyncSession):
        ai_models: List[AIModel] = await self.models()
        saved_models = (await session.execute(select(Model).where(Model.provider_id == self.model_provider.id))).scalars()
        if ai_models and len(ai_models) > 0:
            for ai_model in ai_models:
                if ai_model.id not in [db_model.name for db_model in saved_models]:
                    session.add(
                        create_model_by_class(
                            Model, 
                            consumer, 
                            provider_name = self.model_provider.name, 
                            provider_id = self.model_provider.id,
                            name = ai_model.id,
                            type = ai_model.support_types[0].value,
                            args = ai_model.args
                        )
                    )