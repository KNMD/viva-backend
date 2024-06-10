
from langchain_core.callbacks import AsyncCallbackHandler
from pydantic import BaseModel

from src.schemas.core import AppConfigEntity

class AsyncSSECallbackHandler(AsyncCallbackHandler, BaseModel):
    app_config: AppConfigEntity
    # sender: Sender
