

from sqlalchemy import JSON, TIMESTAMP, UUID, Column, String, func
from .database import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class BaseRepo():
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_by = Column(String(100), nullable=False)
    last_update_at = Column(TIMESTAMP, nullable=True, onupdate=func.now())
    last_update_by = Column(String(100), nullable=True)
    tenant = Column(String(36), nullable=False)

class ModelProvider(Base, BaseRepo):
    __tablename__ = "model_provider"
    id = Column(String(40), primary_key=True)
    name = Column(String(40), nullable=False)
    implement_name = Column(String(40), nullable=False)
    type = Column(String(40), nullable=False)
    assets = Column(JSON, nullable=False)
    credential_schema = Column(JSON, nullable=False)

class Model(Base, BaseRepo):
    __tablename__ = "model"
    id = Column(String(40), primary_key=True)
    provider_name = Column(String(40), nullable=False)
    provider_id = Column(String(40), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(40), nullable=False)
    args = Column(JSON, nullable=True)


class User(Base):
    __tablename__ = "users"

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    id = Column(String(40), primary_key=True)

