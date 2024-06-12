

from typing import Dict

from services.model_provider.base import ModelProviderInstance
from services.model_provider.openai import OpenAIModelProviderInstance


model_provider_mapper: Dict[str, ModelProviderInstance] = {
    "openai": OpenAIModelProviderInstance
}