from fastapi import FastAPI
from pathlib import Path
from utils.app_register import register
from fastapi_pagination import add_pagination
import uvicorn
from . import main_router
from config.settings import app_settings

app = FastAPI()
add_pagination(app)
app.include_router(main_router.router, prefix=f"/engine")
register(app)

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)