from fastapi import FastAPI
from pathlib import Path
from utils.app_register import register
from fastapi_pagination import add_pagination
import uvicorn
from . import main_router
from config.settings import app_settings
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
add_pagination(app)
app.include_router(main_router.router, prefix=f"/engine")
register(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的来源列表。例如：["http://example.org", "https://example.org"]。设置为 ["*"] 以允许所有来源。
    allow_credentials=True,  # 允许携带 cookie
    allow_methods=["*"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的 HTTP 头部
)

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)