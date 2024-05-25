
from database.database import get_db
from database.models import Seed

CATEGORY_HIERARCHY: int = 4
CATEGORY_SEED_KEY_PRIFEX: str = "CATEGORY_HIERARCHY_"
class CommonService:

    @classmethod
    async def increment(cls, key:str):
        async with get_db() as session:
            record = await session.get(Seed, key)
            if record:
                record.value += 1
                return record.value
            else: 
                session.add(Seed(key=key, value=1))
            return 1
        
    @classmethod
    async def category_hierarchy(cls, parent_id: str = None) -> str:
        seed_key = CATEGORY_SEED_KEY_PRIFEX + parent_id if parent_id else CATEGORY_SEED_KEY_PRIFEX + "root"
        seed_val = cls.increment(seed_key)
        if len(str(seed_val)) > CATEGORY_HIERARCHY:
            raise ValueError(f'category hierarchy overflow，hierarchy {CATEGORY_HIERARCHY}, current increasement val: {seed_val}')
        return str(seed_val).zfill(CATEGORY_HIERARCHY)
            

