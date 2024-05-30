
from typing import Type
from pydantic import BaseModel
from ulid import ULID
from database.models import BaseRepo
from schemas.core import Consumer


def model_autofill(model: BaseRepo, consumer: Consumer, **kwargs):
    
    if not model.created_by:
        model.created_by = consumer.id
    if not model.tenant:
        model.tenant = consumer.tenant
    if model.last_update_by:
        model.last_update_by = consumer.id
    
    if hasattr(model, 'id') and not model.id:
        model.id = str(ULID())
    
    if kwargs:
        for key, value in kwargs.items():
            setattr(model, key, value)
    return model

def create_model_by_class(repo_cls: Type[BaseRepo],  consumer: Consumer, entity: BaseModel, **kwargs) -> BaseRepo:

    return repo_cls(
        id = kwargs.get("id", ULID()),
        created_by = consumer.id,
        tenant = consumer.tenant,
        last_update_by = consumer.id,
        last_update_at = None,
        created_at = None,
        **entity.model_dump(),
        **kwargs
    )

        