from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from trainr.backend.api.v1 import v1
from trainr.backend.api.v1.model.health import HealthApiModel
from trainr.backend.handler.database.engine import init_db
from trainr.backend.handler.reading import ReadingHandler

app = FastAPI()

app.include_router(v1, prefix='/api')


@app.on_event('startup')
@repeat_every(seconds=30 * 60)
def expire_reading_history() -> None:
    handler = ReadingHandler()

    handler.remove_history()


@app.on_event('startup')
async def init():
    init_db()


@app.get('/', response_model=HealthApiModel)
async def root():
    return HealthApiModel(healthy=True)
