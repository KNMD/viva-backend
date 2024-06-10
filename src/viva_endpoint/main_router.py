

import asyncio
import datetime
import json
import time
from typing import AsyncIterable, Awaitable
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from loguru import logger
from schemas.core import AppCompletionChunk, AppConfigEntity, AppEntity, AppPreviewIn, CommonResponse, Consumer

from langchain_openai import ChatOpenAI

from pydantic import BaseModel
from openai.types.chat.chat_completion_chunk import Choice, ChoiceDelta
from utils.deps import get_consumer

from viva_endpoint.engine_service import EngineService

router = APIRouter(
    default_response_class=CommonResponse,
    prefix="/app"
)

async def send_message(app_preview: AppPreviewIn, consumer: Consumer) -> AsyncIterable[str]:
    
    task, callback = await EngineService.output(input = app_preview.input, app_config = app_preview.config, consumer = consumer)
    
    try:
        async for token in callback.aiter():
            comletion = AppCompletionChunk(
                id="123",
                object="chat.completion.chunk",
                created=int(time.time()),
                model = "gpt-3.5-turbo-0125",
                choices=[
                    Choice(
                        index=0, 
                        delta=ChoiceDelta(
                            role="assistant",
                            content=token
                        )
                    )
                ]
            )
            yield comletion.to_json() + "\n"
            # yield json.dumps(comletion)
    finally:
        callback.done.set()

    await task



@router.post("/preview")
async def preview(app_preview: AppPreviewIn, consumer = Depends(get_consumer)):
    return StreamingResponse(send_message(app_preview, consumer), media_type="text/event-stream")


