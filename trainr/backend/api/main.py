from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from prometheus_fastapi_instrumentator import Instrumentator

from trainr.backend.api.v1 import v1
from trainr.backend.api.v1.model.light import Color
from trainr.backend.api.v1.model.light import LightColorInputApiModel
from trainr.backend.api.v1.routers.fan import turn_fan_off
from trainr.backend.api.v1.routers.light import set_light_color
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
            reading = await HRReadingHandler().get_reading(seconds=60)
        elif reading_type == ReadingType.FTP:
            reading = await FTPReadingHandler().get_reading(seconds=60)
        else:
            raise NotImplementedError(
                f'Shutting down for reading type {reading_type} not implemented.')

        if reading.reading_value < 1:
            await turn_fan_off()
            await set_light_color(LightColorInputApiModel(color_name=Color.WHITE))


@app.on_event('startup')
async def init():
    init_db()


Instrumentator().instrument(app).expose(app)
