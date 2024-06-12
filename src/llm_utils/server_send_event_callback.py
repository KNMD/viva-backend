
from typing import Any, Dict, List, Optional
from uuid import UUID
from fastapi.responses import StreamingResponse
from langchain_core.callbacks import AsyncCallbackHandler
from loguru import logger
from pydantic import BaseModel
from langchain.schema import BaseMessage

from src.schemas.core import AppConfigEntity

class AsyncSSECallbackHandler(AsyncCallbackHandler, BaseModel):
    app_config: AppConfigEntity
    response: StreamingResponse
    # sender: Sender

    async def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        logger.info("on_chat_model_start...")