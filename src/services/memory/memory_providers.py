from pydantic import ConfigDict, model_validator
import redis.asyncio as redis

from typing import Any, List, Optional
from openai import BaseModel
from schemas.core import Message
from services.memory.base import BaseMessageMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from config.settings import app_settings

class RedisMessageMemory(BaseMessageMemory):
    redis_url: str
    ttl: int
    _client = None

    @model_validator(mode="after")
    def init(self):
        pool = redis.ConnectionPool.from_url(self.redis_url)
        self._client = redis.Redis.from_pool(pool)
        return self

    async def _get(self, key:str) -> List[Message]:
        _items = await self._client.lrange(key, 0, -1)
        items = [Message.model_validate_json(m) for m in _items]
        return items

    async def _put(self, key:str, messages: List[Message]):
        return await self._client.set(key, messages)

    async def _append(self, key: str, messages: List[Message]):
        for message in messages:
            await self._client.rpush(key, message.model_dump_json())
        if self.ttl:
            await self._client.expire(key, self.ttl)