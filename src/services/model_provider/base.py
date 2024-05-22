from abc import ABC, abstractmethod
from typing import List

from schemas.core import AIModel, FormSchema, ModelType


class ModelProviderInstance(ABC):
    
    def validate_provider_credentials(self, credentials: List[FormSchema]) -> bool:
        """
        Validate provider credentials
        """
        raise NotImplementedError
    
    def model_types(self) -> List[ModelType]:
        raise NotImplementedError
    
    
    def models(self) -> List[AIModel]:
        """
        get provider all models
        """
        raise NotImplementedError



