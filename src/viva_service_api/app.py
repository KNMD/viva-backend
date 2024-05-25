from fastapi import FastAPI
from pathlib import Path
from utils.app_register import register
from fastapi_pagination import add_pagination
import models_router as model
import uvicorn

app = FastAPI()
add_pagination(app)
app.include_router(model.router, prefix=f"/viva-service")
register(app)

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)