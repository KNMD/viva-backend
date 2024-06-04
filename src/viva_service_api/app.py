from fastapi import FastAPI
from pathlib import Path
from utils.app_register import register
from fastapi_pagination import add_pagination
import uvicorn
from . import app_router, category_router, models_router, dataset_router
from config.settings import app_settings

app = FastAPI()
add_pagination(app)
app.include_router(app_router.router, prefix=f"/viva-service")
app.include_router(category_router.router, prefix=f"/viva-service")
app.include_router(models_router.router, prefix=f"/viva-service")
app.include_router(dataset_router.router, prefix=f"/viva-service")
register(app)

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)