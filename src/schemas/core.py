import datetime
from typing import Any, Dict, Optional
from pydantic import UUID4, BaseModel


class StandardOut(BaseModel):
    created_at: datetime.datetime
    created_by: str
    last_update_at: Optional[int]
    last_update_by: Optional[str]
    tenant: str

class UserIn(BaseModel):
    name: str
    email: str


class UserOut(UserIn):
    id: UUID4

    class Config:
        from_attributes = True


class ModelOut(StandardOut):
    id: UUID4
    
    

    class Config:
        from_attributes = True