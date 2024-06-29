

from abc import ABC
from openai import BaseModel

from schemas.core import AppEntity, AppInput, InterfaceEntity


class InterfaceInstance(BaseModel, ABC):
    interface_config_entity: InterfaceEntity
    app: AppEntity
    app: AppInput

    async def pre_call(self):
        raise NotImplementedError
    

    async def call_interface(self):
        raise NotImplementedError
    
    async def after_call(self):
        raise NotImplementedError
    