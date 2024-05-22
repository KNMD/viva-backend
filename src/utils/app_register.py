
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
from loguru import logger

from exceptions.exception import AuthenticationError, ForbiddenError, ResponseException, SensitiveError


def register(app):

    @app.exception_handler(AuthenticationError)
    async def authentication_exception_handler(request: Request, e: AuthenticationError):
        return JSONResponse(
            status_code=401,
            content={'message': e.message, 'code': 401},
        )

    @app.exception_handler(ForbiddenError)
    async def forbidden_exception_handler(request: Request, e: ForbiddenError):
        return JSONResponse(
            status_code=403,
            content={'message': e.message, 'code': 403},
        )
        
    @app.exception_handler(SensitiveError)
    async def sensitive_exception_handler(request: Request, e: ForbiddenError):
        return JSONResponse(
            status_code=413,
            content={'message': e.message, 'code': 413},
        )

    @app.exception_handler(ResponseException)
    async def resp_exception_handler(request: Request, e: ResponseException):
        logger.error(f'{request.method} {request.url.path} {repr(e)}')
        return JSONResponse(
            status_code=e.status,
            content={'message': e.message, 'code': e.code, 'error_key': e.error_key},
        )

    @app.exception_handler(HTTPException)
    async def resp_exception_handler(request: Request, e: HTTPException):
        logger.error(f'{request.method} {request.url.path} {repr(e)}')
        return JSONResponse(
            status_code=e.status_code,
            content={'message': e.detail, 'code': 0},
        )

    @app.exception_handler(Exception)
    async def unicorn_exception_handler(request: Request, e: Exception):
        logger.error(f'{request.method} {request.url.path} {repr(e)}')
        return JSONResponse(
            status_code=500,
            content={'message': 'Inernal Server Error', 'code': 500},
        )

    
