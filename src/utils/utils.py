
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
        model.id = ULID()
    
    if kwargs:
        for key, value in kwargs.items():
            setattr(model, key, value)
    return model
    
        