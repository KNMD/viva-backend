

from typing import Any, Dict, List
from sqlalchemy import JSON, TIMESTAMP, UUID, Column, Integer, String, func, Boolean

from schemas.core import Assets, ModelType
from .database import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

# class Base(MappedAsDataclass, DeclarativeBase):
#     pass

class BaseRepo():
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_by = Column(String(100), nullable=False)
    last_update_at = Column(TIMESTAMP, nullable=True, onupdate=func.now())
    last_update_by = Column(String(100), nullable=True)
    tenant = Column(String(36), nullable=False)

class ModelProvider(Base, BaseRepo):
    __tablename__ = "model_provider"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    class_name: Mapped[str] = mapped_column(String(40), nullable=False)
    type: Mapped[str] = mapped_column(String(40), nullable=False)
    assets: Mapped[List[Assets]] = mapped_column(JSON, nullable=True)
    credential_schema: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

class Model(Base, BaseRepo):
    __tablename__ = "model"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    provider_name: Mapped[str] = mapped_column(String(40), nullable=False)
    provider_id: Mapped[str] = mapped_column(String(40), nullable=False)
    name : Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(40), nullable=False)
    context_window: Mapped[int] = mapped_column(Integer, nullable=False)
    support_vision: Mapped[bool] = mapped_column(Boolean, nullable=False)
    args: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)


class User(Base):
    __tablename__ = "users"

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    id = Column(String(40), primary_key=True)

