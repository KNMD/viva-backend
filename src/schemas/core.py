import datetime
from enum import Enum
import json
from typing import Any, Dict, Literal, Optional
import typing
from fastapi.responses import JSONResponse
from pydantic import UUID4, BaseModel

class ResponseEntity(BaseModel):
  code: int
  chain_code: Optional[int]
  error_key: Optional[str]
  message: Optional[str]
  data: Optional[Any]
  
  @classmethod
  def unknown_err(cls):
    return ResponseEntity(
      code=500,
      error_key = "internal_error",
      message = "Internal Error"
    )

  @classmethod
  def agic_unknown_err(cls):
    return ResponseEntity(
      code=500,
      error_key = "agic_unknown_error",
      message = "AIGC unknown error"
    )

class CommonResponse(JSONResponse): 
  def render(self, content: typing.Any) -> bytes:
    responseData = {
      'code': 0,
      'data': content,
      'message': None
    }
    return json.dumps(
        responseData,
        ensure_ascii=False,
        allow_nan=False,
        indent=None,
        separators=(",", ":"),
    ).encode("utf-8")

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
    id: str

    class Config:
        from_attributes = True

class ModelProviderOut(BaseModel):
    id: str
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
    CHAT = "chat"
    GENERATION = "generation"
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


class ModelOut(BaseModel):
    id: str
    provider_name: str
    provider_id: str
    name: str
    type: str
    context_window: int
    support_vision: bool
    args: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
    
class ModelInt(BaseModel):

    name: str
    type: ModelType
    context_window: int
    support_vision: bool
    args: Optional[Dict[str, Any]] = None
