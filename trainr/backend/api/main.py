from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from trainr.backend.api.v1 import v1
from trainr.backend.api.v1.model.health import HealthApiModel
from trainr.backend.handler.database.engine import init_db
from trainr.backend.handler.reading.ftp import FTPReadingHandler
from trainr.backend.handler.reading.hr import HRReadingHandler
from trainr.backend.handler.system.reading_type import SystemReadingTypeHandler
from trainr.utils import ReadingType

app = FastAPI()

app.include_router(v1, prefix='/api')


@app.on_event('startup')
@repeat_every(seconds=30 * 60)
def expire_reading_history() -> None:
    try:
        reading_type = SystemReadingTypeHandler().get_state().setting_value
        if reading_type == ReadingType.HR:
            HRReadingHandler().remove_history()
        elif reading_type == ReadingType.FTP:
            FTPReadingHandler().remove_history()
        else:
            raise NotImplementedError(f'Expiring history for reading type {reading_type} not implemented.')
    except Exception as e:
        print(e.args)


@app.on_event('startup')
async def init():
    init_db()


@app.get('/', response_model=HealthApiModel)
async def root():
    return HealthApiModel(healthy=True)
