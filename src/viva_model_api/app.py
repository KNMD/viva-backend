from fastapi import FastAPI
from pathlib import Path

from fastapi_pagination import add_pagination
import viva_model_api.models_router as model
import uvicorn

app = FastAPI()
add_pagination(app)
app.include_router(model.router, prefix=f"/models")


    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)