from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


from schemas.core import AIModel

from urllib.parse import urlparse

class AppSettings(BaseSettings):

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', protected_namespaces=())

    model_def_url: str = "local:./config/models.yaml"

    model_provider_mapper: Dict[str, str] = {
        "openai": "openai.OpenAIModelProviderInstance"
    }

    message_memory_key_prefix: str = "MESSAGE_MEMORY_KEY_PREFIX_"

    redis_url: str = "redis://dev-host:6379/0"
    
    redis_default_ttl: int = 3000

        


app_settings = AppSettings()