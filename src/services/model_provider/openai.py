

from loguru import logger
from openai import OpenAI
from typing import List

from sqlalchemy import select
from services.model_provider.base import ModelProviderInstance
from schemas.core import AIModel, ModelProviderEntity, ModelType, Consumer
from database.models import Model, ModelProvider


class OpenAIModelProviderInstance(ModelProviderInstance):

    def model_types(self) -> List[str]:
        return [ModelType.LLM, ModelType.TEXT_EMBEDDING, ModelType.SPEECH2TEXT, ModelType.MODERATION, ModelType.TTS, ModelType.TEXT2IMG]
    
    async def validate_provider_credentials(self, model_provider: ModelProvider) -> bool:
        if not model_provider.credential_config:
            return False
        model_list = await self.models(model_provider)
        return len(model_list) > 0
    
    async def models(self, model_provider: ModelProvider) -> List[AIModel]:
        
        client = OpenAI()

        model_list = client.models.list()
        return model_list
        