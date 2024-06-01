
from typing import Dict, Optional
from fastapi import Request
from loguru import logger
import schemas.error_code as err
from pydantic import BaseModel
from schemas.core import  ResponseEntity


class AuthenticationError(Exception):

    def __init__(self, message: str = 'Unauthorized'):
        self.message = message

class ForbiddenError(Exception):

    def __init__(self, message: str = 'Forbidden'):
        self.message = message
        
class SensitiveError(Exception):

    def __init__(self, message: str = 'Sensitive'):
        self.message = message


class ResponseException(Exception):
  code: int
  status: int
  message: str
  error_key: Optional[str]

  def __init__(self, message: str = 'ResponseException', status:int = 400, code:int = -1, error_key: Optional[str] = None):
    self.code = code
    self.status = status
    self.error_key = error_key
    self.message = message

  @classmethod
  def err(cls, message: str = "Internal Error", status = 500, code = -1, error_var: Optional[str] = None):
    error_key = None
    if error_var != None:
        error_key = error_var
        code = eval(f"err.{error_var}")
        message = None
    return ResponseException(message, status, code, error_key)
