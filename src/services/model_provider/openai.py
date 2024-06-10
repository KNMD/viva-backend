

from langchain_openai import ChatOpenAI
from loguru import logger
from openai import OpenAI, AuthenticationError
from typing import List
import openai

from sqlalchemy import select
from services.model_provider.base import ModelProviderInstance
from schemas.core import AIModel, AppConfigEntity, ModelProviderEntity, ModelType, Consumer
from database.models import Model, ModelProvider
from openai.types import Model as OAIModel
from langchain_core.language_models.base import BaseLanguageModel


class OpenAIModelProviderInstance(ModelProviderInstance):

    def model_types(self) -> List[str]:
        return [ModelType.LLM, ModelType.TEXT_EMBEDDING, ModelType.SPEECH2TEXT, ModelType.MODERATION, ModelType.TTS, ModelType.TEXT2IMG]
    
    async def validate_provider_credentials(self, model_provider: ModelProvider) -> bool:
        if not model_provider.credential_config:
            return False
        try:
            model_list = await self.remove_models(model_provider)
        except AuthenticationError as e:
            logger.error("openai AuthenticationError: {}", e)
            return False
        return len(model_list) > 0
    
    
    async def remove_models(self, model_provider: ModelProvider) -> List[OAIModel]:
        
        client = OpenAI(
            organization=model_provider.credential_config.get("org_id", None),
            base_url=model_provider.credential_config.get("api_base", None),
            api_key=model_provider.credential_config.get("api_key", None),
        )

        model_list = []
        for item in client.models.list().data:
            if item.owned_by == 'openai':
                model_list.append(item)
            

        return model_list
    

        

    async def model_impl(self, model: Model, app_config: AppConfigEntity) -> BaseLanguageModel:
        model = ChatOpenAI(
            base_url="https://api.aihubmix.com/v1",
            api_key="sk-Fr57TA861M7kpFuq7d963a83095e46A4Ab5809C6E9EdD304",
            streaming=True,
            model="gpt-3.5-turbo-0125",
        )

        return model