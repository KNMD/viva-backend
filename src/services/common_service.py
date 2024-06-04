
from pathlib import Path
from typing import Dict, List
from database.database import get_db
from database.models import Seed
from sqlalchemy.ext.asyncio import AsyncSession
import urllib.request
import yaml
from schemas.core import AIModel
from config.settings import app_settings


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
    def do_load_models_definition(cls, model_def_url = None) -> Dict[str, List[AIModel]]:
        if not model_def_url:
            model_def_url = app_settings.model_def_url
        yaml_data = None
        if model_def_url.startswith("local:"):
            relative_path = Path(model_def_url[6:]).resolve()
            with open(relative_path, 'r') as file:
                yaml_data = file.read()
        else:
            with urllib.request.urlopen(model_def_url) as response:
                yaml_data = response.read()
        data = yaml.safe_load(yaml_data)
        def_data = {}
        for k, v in data.items():
            ai_models = []
            for m in v:
                ai_models.append(AIModel(**m))
            def_data[k] = ai_models

        return def_data
