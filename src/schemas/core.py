import datetime
from enum import Enum
import json
from typing import Any, Dict, List, Literal, Optional, Union
import typing
from fastapi.responses import JSONResponse
from pydantic import UUID4, BaseModel, ConfigDict


class NamespaceConfig:
    model_config = ConfigDict(protected_namespaces=())
    pass

class ResponseEntity(BaseModel):
  code: int
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

class StandardEntity(BaseModel):
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

class ModelProviderEntity(StandardEntity):
    id: str
    name: str
    type: str
    class_name: str
    assets: Optional[Assets]

    class Config:
        from_attributes = True

class BaseCredential(BaseModel):
    class Config:
        from_attributes = True

class OpenAICredential(BaseCredential):
    type: Literal["openai"]
    api_key: str
    api_base: Optional[str] = None
    org_id: Optional[str] = None


class ModelProviderIn(BaseModel):
    name: str
    type: Literal["self", "custom"]
    assets: Optional[Assets] = None
    credential_config: Optional[BaseCredential] = None
    support_model_sync: bool = False

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


class FormType(Enum):
    """
    Enum class for form type.
    """
    TEXT_INPUT = "text-input"
    SECRET_INPUT = "secret-input"
    SELECT = "select"
    RADIO = "radio"
    SWITCH = "switch"
    API = "api"

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
    api_id: Optional[str]
    # show_on: list[FormShowOnObject] = []



class ModelOut(StandardEntity):
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

class CategoryEntity(BaseModel):
    id: Optional[str] = None
    name: str
    parent_id: Optional[str] = None
    assets: Optional[Assets] = None
    plugin: str
    ext: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class StartupEnhancer(BaseModel):
    prompt: str
    selections: Optional[List[str]] = None

class SuggestionEnhancer(NamespaceConfig, BaseModel):
    model_id: str
    prompt: str

class TextToSpeechEnhancer(NamespaceConfig, BaseModel):
    model_id: str
    language: str
    voicer: str

class SpeechToTextEnhancer(NamespaceConfig, BaseModel):
    model_id: str
    stream_support: bool

class ChatEnhancer(BaseModel):
    enabled: bool
    type: Literal["startup", "suggestion", "tts", "stt"]
    settings: Union[StartupEnhancer, SuggestionEnhancer, TextToSpeechEnhancer, SpeechToTextEnhancer]

class QueryEnchancer(NamespaceConfig, BaseModel):
    prompt: str
    model_id: str

class RagConfig(BaseModel):
    datasets: List[str]
    type: Literal["auto_prompt_append", "use_app_prompt"]
    query_enhancer: Optional[QueryEnchancer] = None
    

class AppConfigEntity(BaseModel):
    base_model_id: str
    prompt: str
    variables: List[FormSchema]
    chat_enhancer: Optional[ChatEnhancer] = None
    rag_config: Optional[RagConfig] = None
    

class AppEntity(StandardEntity):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    assets: Optional[Assets] = None
    category_id: Optional[str] = None
    app_config: Optional[AppConfigEntity] = None
    status: Optional[int] = 0
    plugin: Optional[str] = None
    ext: Optional[Dict[str, Any]] = None
    class Config:
        from_attributes = True
class AppEntityPatch(AppEntity):
    name: Optional[str] = None

class DatasetEntity(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    assets: Optional[Assets] = None
    category_id: Optional[str] = None
    embedding_model: str
    embedding_model_provider: str
    retrieval_model: Optional[str]


