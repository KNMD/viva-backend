import datetime
from enum import Enum
import json
from typing import Any, Dict, List, Literal, Optional, Union
import typing
from fastapi.responses import JSONResponse
from pydantic import UUID4, BaseModel, ConfigDict, field_serializer
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from langchain.schema import ChatMessage

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


    @field_serializer('created_at', 'last_update_at')
    def serialize_dt(self, field: datetime.datetime, _info):
        if field:
            return int(field.timestamp() * 1000)
        else: 
            return None

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


class BaseCredential(BaseModel):
    class Config:
        from_attributes = True

class OpenAICredential(BaseCredential):
    type: Literal["openai"]
    api_key: str
    api_base: Optional[str] = None
    org_id: Optional[str] = None

class ModelProviderEntity(StandardEntity):
    id: str
    name: str
    type: str
    class_name: str
    assets: Optional[Assets] = None
    credential_config: Optional[Union[OpenAICredential]] = None

    class Config:
        from_attributes = True



class ModelProviderIn(BaseModel):
    name: str
    type: Literal["self", "custom"]
    assets: Optional[Assets] = None
    credential_config: Optional[Union[OpenAICredential]] = None

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


class AIModel(BaseModel):
    id: str
    support_types: List[ModelType]
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
    SLIDER = "slider"
    API = "api"

class FormOption(BaseModel):
    """
    form option.
    """
    label: str
    value: str

class SLiderConstraint(BaseModel):
    type: Literal['slider']
    max: float
    min: float
    step: float = 0.1

class FormSchema(BaseModel):
    """
    form schema.
    """
    variable: str
    label: str
    type: FormType
    required: bool = True
    default: Optional[Any] = None
    options: Optional[List[FormOption]] = None
    placeholder: Optional[str] = None
    max_length: int = 0
    api_id: Optional[str] = None
    constraint: Optional[Union[SLiderConstraint]] = None
    description: Optional[str] = None
    # show_on: list[FormShowOnObject] = []


class ModelDefinitioin(BaseModel):
    display_args: Dict[str, List[FormSchema]]
    models: List[AIModel]



class ModelEntity(StandardEntity):
    id: str
    provider_name: str
    provider_id: str
    name: str
    type: str
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

class Message(BaseModel):
    role: Optional[str] = "user"
    content: str

class AppConfigEntity(BaseModel):
    base_model_id: str
    prompt: str
    variables: Optional[List[FormSchema]] = None
    chat_enhancer: Optional[ChatEnhancer] = None
    rag_config: Optional[RagConfig] = None

class AppInput(BaseModel):
    conversation_id: Optional[str] = None
    messages: List[Message]
    variable_vals: Dict[str, Any] = None
    

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



class AppCompletionChunk(ChatCompletionChunk):
    
    object: Literal["chat.completion.chunk", "image.generation", "speech.generation", "voice.transcript", "html.generation"]
    
class AppPreviewIn(BaseModel):
    input: AppInput
    config: AppConfigEntity


