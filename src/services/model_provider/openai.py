


from typing import List
from base import ModelProviderInstance
from schemas.core import ModelType


class OpenAIModelProvider(ModelProviderInstance):

    def model_types(self) -> List[str]:
        return [ModelType.LLM, ModelType.TEXT_EMBEDDING, ModelType.SPEECH2TEXT, ModelType.MODERATION, ModelType.TTS, ModelType.TEXT2IMG]