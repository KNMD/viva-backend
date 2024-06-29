

from loguru import logger
from services.interface_impl.base import InterfaceInstance
import httpx

class HttpInterfaceInstance(InterfaceInstance):
    
    async def pre_call(self):
        logger.debug("http interface pre call: {}", self.interface_config_entity)
    

    async def call_interface(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            print(resp.status_code)

    
    async def after_call(self):
        logger.debug("http interface after call: {}", self.interface_config_entity)