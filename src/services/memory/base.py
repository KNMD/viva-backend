

from abc import ABC
from typing import Any, Dict, List
from openai import BaseModel
from pydantic import ConfigDict
from sqlalchemy import select
from ulid import ULID
from schemas.core import AppEntity, Consumer, Message, ModelEntity, ModelProviderEntity
from config.settings import app_settings
from database.database import open_session
from database.models import Message as DBMessage
from openai.types.completion_usage import CompletionUsage

class BaseMessageMemory(BaseModel, ABC):
    model_config = ConfigDict(protected_namespaces=())

    conversation_id: str
    consumer: Consumer
    app: AppEntity
    model_provider: ModelProviderEntity
    model: ModelEntity

    def _make_key(self) -> str:
        return f"{app_settings.message_memory_key_prefix}{self.consumer.tenant}_{self.conversation_id}"
    
    async def retrieval(self) -> List[Message]: 
        key = self._make_key()
        messages = await self._get(key)
        if not messages or len(messages) == 0:
            messages = await self.store_retrieval()
        return messages
    
    async def store_retrieval(self) -> List[Message]:
        async with open_session() as session:
            db_messages = (await session.execute(
                select(DBMessage)
                .where(DBMessage.conversation_id == self.conversation_id)
                .where(DBMessage.tenant == self.consumer.tenant))).scalars()
            return [Message(role=m.type, content=m.content) for m in db_messages]
    
    async def store(self, messages: List[Message]):
        key = self._make_key()
        return await self._put(key, messages)

    async def append(self, messages: List[Message]):
        key = self._make_key()
        await self._append(key, messages)
        async with open_session() as session:
            db_messages = [ DBMessage(
                        id = str(ULID()),
                        app_id = self.app.id,
                        app_name = self.app.name,
                        conversation_id = self.conversation_id,
                        conversation_name = f'{self.app.name}_preview',
                        model_provider_id = self.model_provider.id,
                        model_provider_name = self.model_provider.name,
                        model_id = self.model.id,
                        model_name = self.model.name,
                        type = message.role,
                        content = message.content,
                        token = message.token if message.token != None else len(message.content),
                        tenant = self.consumer.tenant,
                        created_by = self.consumer.id,
                        created_at = None,
                        worfklow_id = None,
                        workflow_instance_id = None,
                        node_info = None,
                        error = None
                ) for message in messages]
            session.add_all(db_messages)
                
                