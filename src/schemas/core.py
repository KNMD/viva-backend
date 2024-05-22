import datetime
from enum import Enum
from typing import Any, Dict, Literal, Optional
from pydantic import UUID4, BaseModel


class StandardOut(BaseModel):
    created_at: datetime.datetime
    created_by: str
    last_update_at: Optional[datetime.datetime]
    last_update_by: Optional[str]
    tenant: str

class Consumer(BaseModel):
    id: str
    name: str
    tenant: str

class ImageURL(BaseModel):
    url: str
    high: Optional[str]
    low: Optional[str]

class Assets(BaseModel):
    image: ImageURL 
    type: Literal["square", "landscape", "portrait"]

class UserIn(BaseModel):
    name: str
    email: str


class UserOut(UserIn):
    id: UUID4

    class Config:
        from_attributes = True

class ModelProviderOut(BaseModel):
    id: UUID4
    name: str
    type: str
    class_name: str
    assets: Optional[Assets]

    class Config:
        from_attributes = True

class ModelProviderIn(BaseModel):
    name: str
    type: Literal["self", "custom"]
    assets: Optional[Assets] = None
    class_name: str

class ModelType(Enum):
    """
    Enum class for model type.
    """
    LLM = "llm"
    TEXT_EMBEDDING = "text-embedding"
    RERANK = "rerank"
    SPEECH2TEXT = "speech2text"
    MODERATION = "moderation"
    TTS = "tts"
    TEXT2IMG = "text2img"
    CLASSIFICATION = "classification"


class AIModel(BaseModel):
    name: str
    type: ModelType
    args: Optional[Dict[str, Any]]

class ModelOut(StandardOut, AIModel):
    id: UUID4
    provider_name: str
    provider_id: str
    
    

    class Config:
        from_attributes = True

class FormType(Enum):
    """
    Enum class for form type.
    """
    TEXT_INPUT = "text-input"
    SECRET_INPUT = "secret-input"
    SELECT = "select"
    RADIO = "radio"
    SWITCH = "switch"

class FormOption(BaseModel):
    """
    form option.
    """
    label: str
    value: str

class FormSchema(BaseModel):
    """
    form schema.
    """
    variable: str
    label: str
    type: FormType
    required: bool = True
    default: Optional[str] = None
    options: Optional[list[FormOption]] = None
    placeholder: Optional[str] = None
    max_length: int = 0
    # show_on: list[FormShowOnObject] = []

