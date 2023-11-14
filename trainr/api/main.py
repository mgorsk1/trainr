from fastapi import FastAPI

from trainr.handler.database.engine import init_db
from trainr.api.v1 import v1
from trainr.api.v1.model.health import HealthApiModel

app = FastAPI()

app.include_router(v1, prefix='/api')

# @todo add background task to clear reading history


@app.on_event('startup')
async def init():
    init_db()


@app.get('/', response_model=HealthApiModel)
async def root():
    return HealthApiModel(healthy=True)
