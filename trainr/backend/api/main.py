from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from trainr.backend.api.v1 import v1
from trainr.backend.api.v1.routers.fan import turn_fan_off
from trainr.backend.api.v1.routers.light import turn_light_off
from trainr.backend.handler.database.engine import init_db
from trainr.backend.handler.reading.ftp import FTPReadingHandler
from trainr.backend.handler.reading.hr import HRReadingHandler
from trainr.backend.handler.system.mode import SystemModeHandler
from trainr.backend.handler.system.reading_type import SystemReadingTypeHandler
from trainr.utils import ReadingType


app = FastAPI(
    title='Trainr API',
    summary='Backend API for managing application for Indoor Training Automation.',
    contact={
        'name': 'Mariusz Górski',
        'url': 'https://www.mariuszgorski.pl',
        'email': 'gorskimariusz13@gmail.com',
    },
    license_info={
        'name': 'Apache 2.0',
        'identifier': 'MIT',
    },
)

app.include_router(v1, prefix='/api')


@app.on_event('startup')
@repeat_every(seconds=60)
async def shut_down():
    system_on = SystemModeHandler().get_state().setting_value == 'AUTO'
    reading_type = SystemReadingTypeHandler().get_state().setting_value

    if system_on:
        if reading_type == ReadingType.HR:
            reading = HRReadingHandler().get_reading(seconds=60)
        elif reading_type == ReadingType.FTP:
            reading = FTPReadingHandler().get_reading(seconds=60)
        else:
            raise NotImplementedError(
                f'Shutting down for reading type {reading_type} not implemented.')

        if reading.reading_value < 1:
            await turn_fan_off()
            await turn_light_off()


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
            raise NotImplementedError(
                f'Expiring history for reading type {reading_type} not implemented.')
    except Exception as e:
        print(e.args)


@app.on_event('startup')
async def init():
    init_db()
