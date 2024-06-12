

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
from utils.utils import messages_to_lc_message
from utils.deps import get_consumer
from langchain.callbacks import AsyncIteratorCallbackHandler
from viva_endpoint.engine_service import EngineService

router = APIRouter(
    default_response_class=CommonResponse,
    prefix="/app"
)

async def send_message(app_preview: AppPreviewIn, consumer: Consumer) -> AsyncIterable[str]:
    
    # task, callback = await EngineService.output(input = app_preview.input, app_config = app_preview.config, consumer = consumer)
    model = ChatOpenAI(
        base_url="https://api.aihubmix.com/v1",
        api_key="sk-Fr57TA861M7kpFuq7d963a83095e46A4Ab5809C6E9EdD304",
        streaming=True,
        model="gpt-3.5-turbo-0125",
    )
    callback = AsyncIteratorCallbackHandler()
    # task = asyncio.create_task(
    await model.agenerate(messages=[ messages_to_lc_message(app_preview.input.messages) ], callbacks=[callback])
        # )
    
    
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
            logger.info("comletion: {}", comletion)
            yield comletion.to_json() + "\n"
            # yield json.dumps(comletion)
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        callback.done.set()

    # await task



@router.post("/preview")
async def preview(app_preview: AppPreviewIn, consumer = Depends(get_consumer)):
    return StreamingResponse(send_message(app_preview, consumer), media_type="text/event-stream")


