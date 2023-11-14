from fastapi import FastAPI

from trainr.api.v1 import v1
from trainr.api.v1.model.health import HealthApiModel

app = FastAPI()

app.include_router(v1, prefix='/api')

# @todo add background task to clear reading history


@app.get('/', response_model=HealthApiModel)
async def root():
    return HealthApiModel(healthy=True)
