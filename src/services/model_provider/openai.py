

from langchain_openai import ChatOpenAI
from loguru import logger
from openai import AsyncOpenAI, AsyncStream, OpenAI, AuthenticationError
from typing import List
import openai

from sqlalchemy import select
from services.model_provider.base import ModelProviderInstance
from schemas.core import AIModel, AppConfigEntity, Message, ModelProviderEntity, ModelType, Consumer
from database.models import Model, ModelProvider
from openai.types import Model as OAIModel
from langchain_core.language_models.base import BaseLanguageModel
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

class OpenAIModelProviderInstance(ModelProviderInstance):

    def model_types(self) -> List[str]:
        return [ModelType.LLM, ModelType.TEXT_EMBEDDING, ModelType.SPEECH2TEXT, ModelType.MODERATION, ModelType.TTS, ModelType.TEXT2IMG]
    
    async def validate_provider_credentials(self) -> bool:
        if not self.model_provider.credential_config:
            return False
        try:
            model_list = await self.remote_models()
        except Exception as e:
            logger.error("openai AuthenticationError: {}", e)
            return False
        return len(model_list) > 0
    
    
    async def remote_models(self) -> List[OAIModel]:
        
        client = OpenAI(
            organization=self.model_provider.credential_config.org_id,
            base_url=self.model_provider.credential_config.api_base,
            api_key=self.model_provider.credential_config.api_key,
        )

        model_list = []
        for item in client.models.list().data:
            if item.owned_by == 'openai':
                model_list.append(item)
            

        return model_list
    

        

    async def model_impl(self, model: Model, app_config: AppConfigEntity) -> BaseLanguageModel:
        model = ChatOpenAI(
            base_url=self.model_provider.credential_config.api_base,
            api_key=self.model_provider.credential_config.api_key,
            streaming=True,
            model=model.name,
        )

        return model
    
    async def _agenerate(self, model: Model, app_config: AppConfigEntity, messages: List[Message]) ->  ChatCompletion | AsyncStream[ChatCompletionChunk]:
        
        client = AsyncOpenAI(
            base_url=self.model_provider.credential_config.api_base,
            api_key=self.model_provider.credential_config.api_key,
        )
        return await client.chat.completions.create(
            model=model.name,
            messages=messages,
            stream=True,
        )