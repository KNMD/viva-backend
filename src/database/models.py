

import datetime
from typing import Any, Dict, List
from sqlalchemy import JSON, TIMESTAMP, UUID, Column, Index, Integer, Numeric, String, Text, func, Boolean

# from schemas.core import Assets, ModelType
# from .database import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class BaseRepo():
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    created_by: Mapped[str] = mapped_column(String(100), nullable=False)
    last_update_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=True, onupdate=func.now())
    last_update_by: Mapped[str] = mapped_column(String(100), nullable=True)
    tenant: Mapped[str] = mapped_column(String(36), nullable=False)


class Seed(Base):
  __tablename__ = "seed"
  key: Mapped[str] = mapped_column(String(100), primary_key=True)
  val: Mapped[int] = mapped_column(Integer, nullable=False, server_default='0')
    

class ModelProvider(Base, BaseRepo):
    __tablename__ = "model_provider"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    class_name: Mapped[str] = mapped_column(String(40), nullable=False)
    type: Mapped[str] = mapped_column(String(40), nullable=False)
    assets: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
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

model_model_provider_index = Index('model_model_provider_tenent_index', Model.provider_id, Model.tenant, unique=False)

class User(Base):
    __tablename__ = "users"

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    id = Column(String(40), primary_key=True)


class App(Base, BaseRepo):
    __tablename__ = "app"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    assets: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    category_id: Mapped[str] = mapped_column(String(4000), nullable=True)
    # app_config_id: Mapped[str] = mapped_column(String(255), nullable=True)
    app_config: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    """
    -1 disabled, 0 editing, 1 public 2 private
    """
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    
    plugin: Mapped[str] = mapped_column(String(50), nullable=True, index=True)

    ext: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

app_category_tenant_index = Index('app_category_tenant_index', App.category_id, App.tenant, unique=False)

class Dataset(Base, BaseRepo):
    __tablename__ = "dataset"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    assets: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    category_id: Mapped[str] = mapped_column(String(255), nullable=True)
    embedding_model: Mapped[str] = mapped_column(String(255), nullable=False)
    embedding_model_provider: Mapped[str] = mapped_column(String(255), nullable=False)
    retrieval_model: Mapped[str] = mapped_column(String(255), nullable=False)
dataset_category_tenant_index = Index('dataset_category_tenant_index', Dataset.category_id, Dataset.tenant, unique=False)

class Doucument(Base, BaseRepo):
    __tablename__ = 'documents'
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(40), nullable=False)
    dataset_id: Mapped[str] = mapped_column(String(255), nullable=False)
    process_rule: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    """
    0 uploaded, 1 processing, 2 error 3 success
    """
    progress: Mapped[int] = mapped_column(Integer, nullable=False)
    process_status_detail: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    process_error_message: Mapped[str] = mapped_column(Text, nullable=True)
    word_count: Mapped[int] = mapped_column(Integer, nullable=True)
    images_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    complete_at = mapped_column(TIMESTAMP, nullable=True)
document_dataset_tenant_index = Index('document_dataset_tenant_index', Doucument.dataset_id, Doucument.tenant, unique=False)

class DocumentSegment(Base, BaseRepo):
    __tablename__ = 'document_segments'
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    dataset_id: Mapped[str] = mapped_column(String(255), nullable=False)
    document_id: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text)
    word_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # indexing fields
    doc_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    """
    0 uploaded, 1 processing, 2 error 3 success
    """
    progress: Mapped[int] = mapped_column(Integer, nullable=False)
    process_status_detail: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    process_error_message: Mapped[str] = mapped_column(Text, nullable=True)
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
document_segment_document_tenant_index = Index('document_segment_dataset_tenant_index', DocumentSegment.document_id, DocumentSegment.tenant, unique=False)


class AppRecycle(Base, BaseRepo):
    __tablename__ = "app_recycle"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    assets: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    category_id: Mapped[str] = mapped_column(String(4000), nullable=True)
    app_config_id: Mapped[str] = mapped_column(String(255), nullable=True)
    """
    -1 disabled, 0 editing, 1 public 2 private
    """
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    
    plugin: Mapped[str] = mapped_column(String(50), nullable=True, index=True)

    ext: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    app_config = mapped_column(JSON, nullable=False)

class AppConfig(Base, BaseRepo):
    __tablename__ = "app_config"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    config_detail = mapped_column(JSON, nullable=False)
    app_id: Mapped[str] = mapped_column(String(40), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
app_config_app_tenant_index = Index('app_config_app_tenant_index', AppConfig.tenant, AppConfig.app_id, unique=False)


class Category(Base, BaseRepo):
    __tablename__ = "category"
    id: Mapped[str] = mapped_column(String(400), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[str] = mapped_column(String(100), nullable=True)
    assets: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    """self or others in plugin table"""
    plugin: Mapped[str] = mapped_column(String(50), nullable=True, index=True)
    ext: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
category_tenant_index = Index('category_tenant_index', Category.tenant, unique=False)
# 

class Conversation(Base, BaseRepo):
    __tablename__ = 'conversation'
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    app_id: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(40), nullable=True)
    app_config_created: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    runtime_args: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
conversation_tenant_app_index = Index('conversation_tenant_app_index', Conversation.tenant, Conversation.app_id, unique=False)

class Plugins(Base, BaseRepo):
    __tablename__ = 'plugins'
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    """
    0 self, 1 thirdparty
    """
    type: Mapped[int] = mapped_column(Integer)
    menu_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    embed_index_url: Mapped[str] = mapped_column(String(500), nullable=True)
    sub_menus: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    plugin_sdk_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    plugin_sdk_initial_code: Mapped[str] = mapped_column(Text, nullable=True)
    workflow_node_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    workflow_node_config: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    message_callback_url: Mapped[str] = mapped_column(String(500), nullable=True)
    diabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
plugins_tenant_index = Index('plugins_tenant_index', Plugins.tenant, unique=False)


class Message(Base):
    __tablename__ = 'messages'
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    app_id: Mapped[str] = mapped_column(String(40))
    app_name: Mapped[str] = mapped_column(String(255), nullable=False)
    conversation_id: Mapped[str] = mapped_column(String(40))
    conversation_name: Mapped[str] = mapped_column(String(255))
    model_provider_id: Mapped[str] = mapped_column(String(40))
    model_provider_name: Mapped[str] = mapped_column(String(255), nullable=False)
    model_id: Mapped[str] = mapped_column(String(40))
    model_name: Mapped[str] = mapped_column(String(255), nullable=False)
    worfklow_id: Mapped[str] = mapped_column(String(40), nullable=True)
    workflow_instance_id: Mapped[str] = mapped_column(String(40), nullable=True)
    node_info: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    type: Mapped[str] = mapped_column(String(40))
    content: Mapped[str] = mapped_column(Text)
    tokens: Mapped[str] = mapped_column(Integer, nullable=False)
    
    error : Mapped[str] = mapped_column(Text, nullable=True)
    
    
    tenant = Column(String(36), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_by = Column(String(100), nullable=False)
messaage_tenant_app_index = Index('messaage_tenant_app_index', Message.tenant, Message.app_id, unique=False)
messaage_tenant_app_conversation_index = Index('messaage_tenant_app_conversation_index', Message.tenant, Message.app_id, Message.conversation_id, unique=False)

    
class RuntimeLog(Base):
    __tablename__ = 'runtime_log'
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    app_id: Mapped[str] = mapped_column(String(40))
    app_name: Mapped[str] = mapped_column(String(255), nullable=False)
    conversation_id: Mapped[str] = mapped_column(String(40))
    conversation_name: Mapped[str] = mapped_column(String(255))
    message_id: Mapped[str] = mapped_column(String(40)) 
    message_content: Mapped[str] = mapped_column(Text)
    message_type: Mapped[str] = mapped_column(String(40))

    model_provider_id: Mapped[str] = mapped_column(String(40))
    model_provider_name: Mapped[str] = mapped_column(String(255), nullable=False)
    model_id: Mapped[str] = mapped_column(String(40))
    model_name: Mapped[str] = mapped_column(String(255), nullable=False)
    worfklow_id: Mapped[str] = mapped_column(String(40), nullable=True)
    workflow_instance_id: Mapped[str] = mapped_column(String(40), nullable=True)
    node_info: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    run_args: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    from_message_id: Mapped[str] = mapped_column(String, nullable=False)
    plugin: Mapped[str] = mapped_column(String(100), nullable=False)
    tenant = Column(String(36), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_by = Column(String(100), nullable=False)
runtime_log_message_index = Index('runtime_log_tenant_message_index', RuntimeLog.message_id, unique=False)

class ExpenseUsage(Base):
   __tablename__ = "expense_usage"
   id: Mapped[str] = mapped_column(String(40), primary_key=True)
   
   tenant_id: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
   user_id: Mapped[str] = mapped_column(String(40), nullable=False)
   token_usage: Mapped[int] = mapped_column(Integer, nullable=False)
   count_usage: Mapped[int] = mapped_column(Integer, nullable=False)
   spend_time_usage: Mapped[int] = mapped_column(Integer, nullable=False)
   

class ExpenseLog(Base):
    __tablename__ = 'expense_log'
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    app_id: Mapped[str] = mapped_column(String(40))
    app_name: Mapped[str] = mapped_column(String(255), nullable=False)
    conversation_id: Mapped[str] = mapped_column(String(40))
    conversation_name: Mapped[str] = mapped_column(String(255))
    message_id: Mapped[str] = mapped_column(String(40)) 
    message_content: Mapped[str] = mapped_column(Text)
    message_type: Mapped[str] = mapped_column(String(40))
    """
    MODEL, API
    """
    type: Mapped[str] = mapped_column(String, nullable=False)
    model_provider_id: Mapped[str] = mapped_column(String(40))
    model_provider_name: Mapped[str] = mapped_column(String(255), nullable=False)
    model_id: Mapped[str] = mapped_column(String(40))
    model_name: Mapped[str] = mapped_column(String(255), nullable=False)
    inputs: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    outputs: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    input_tokens: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    output_tokens: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    model_provider_input_unit_price: Mapped[float] = mapped_column(Numeric(10, 7), nullable=True)
    model_provider_output_unit_price: Mapped[float] = mapped_column(Numeric(10, 7), nullable=True)
    currency: Mapped[str] = mapped_column(String(40), nullable=True)
    input_unit_price: Mapped[float] = mapped_column(Numeric(10, 7), nullable=True)
    output_unit_price: Mapped[float] = mapped_column(Numeric(10, 7), nullable=True)
    tenant = Column(String(36), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    created_by = Column(String(100), nullable=False)

expense_log_tenant_index = Index('expense_log_tenant_index', ExpenseLog.tenant, unique=False)
expense_log_tenant_app_index = Index('expense_log_tenant_app_index', ExpenseLog.tenant, ExpenseLog.app_id, unique=False)
expense_log_tenant_model_index = Index('expense_log_tenant_model_index', ExpenseLog.tenant, ExpenseLog.model_id, unique=False)


