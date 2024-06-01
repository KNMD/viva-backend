
from database.database import get_db
from database.models import Seed
from sqlalchemy.ext.asyncio import AsyncSession

from services.model_provider.base import ModelProviderInstance
from services.model_provider.openai import OpenAIModelProviderInstance
model_provider_mapper = {
    "openai": OpenAIModelProviderInstance
}
CATEGORY_HIERARCHY: int = 4
CATEGORY_SEED_KEY_PRIFEX: str = "CATEGORY_HIERARCHY_"
class CommonService:

    @classmethod
    async def increment(cls, db: AsyncSession, key:str):
        record = await db.get(Seed, key)
        if record:
            record.val += 1
            return record.value
        else: 
            db.add(Seed(key=key, val=1))
        return 1
            
        
    @classmethod
    async def category_hierarchy(cls, db: AsyncSession, parent_id: str = None) -> str:
        seed_key = CATEGORY_SEED_KEY_PRIFEX + parent_id if parent_id else CATEGORY_SEED_KEY_PRIFEX + "root"
        seed_val = await cls.increment(db, seed_key)
        if len(str(seed_val)) > CATEGORY_HIERARCHY:
            raise ValueError(f'category hierarchy overflow，hierarchy {CATEGORY_HIERARCHY}, current increasement val: {seed_val}')
        return str(seed_val).zfill(CATEGORY_HIERARCHY)
    

    @classmethod
    def model_provider_mapper(cls, provider_name: str) -> ModelProviderInstance:
        return model_provider_mapper[provider_name]
            

