from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from prometheus_fastapi_instrumentator import Instrumentator

from trainr.backend.api.v1 import v1
from trainr.backend.api.v1.model.light import Color
from trainr.backend.api.v1.model.light import LightColorInputApiModel
from trainr.backend.api.v1.routers.fan import turn_fan_off
from trainr.backend.api.v1.routers.light import set_light_color
from trainr.backend.config import config
from trainr.backend.handler.database.engine import init_db
from trainr.backend.handler.factory import MotivationHandlerFactory
from trainr.backend.handler.reading.ftp import FTPReadingHandler
from trainr.backend.handler.reading.hr import HRReadingHandler
from trainr.backend.handler.system.settings.coach import \
    SystemMotivationCoachHandler
from trainr.backend.handler.system.settings.coach import \
    SystemMotivationHandler
from trainr.backend.handler.system.settings.mode import SystemModeHandler
from trainr.backend.handler.system.settings.reading_type import \
    SystemReadingTypeHandler
from trainr.backend.handler.system.state.training_on import TrainingOnHandler
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
    training_on = TrainingOnHandler().get_state().setting_value == 'true'
    reading_type = SystemReadingTypeHandler().get_state().setting_value

    if system_on and training_on:
        if reading_type == ReadingType.HR:
            handler = HRReadingHandler()
        elif reading_type == ReadingType.FTP:
            handler = FTPReadingHandler()
        else:
            raise NotImplementedError(
                f'Shutting down for reading type {reading_type} not implemented.')

        reading = await handler.get_reading(seconds=60)

        if reading.reading_value < 1 and training_on:
            coach_name = SystemMotivationCoachHandler().get_state().setting_value

            handler = MotivationHandlerFactory(
                config.motivation).get_handler()

            handler.say_goodbye(coach_name)

            await turn_fan_off()
            await set_light_color(LightColorInputApiModel(color_name=Color.WHITE))
            TrainingOnHandler().set_value("false")


@app.on_event('startup')
async def init():
    init_db()


@app.on_event('startup')
@repeat_every(seconds=60 * 10)
async def coach():
    motivation_enabled = SystemMotivationHandler().get_state().setting_value == 'true'
    training_on = TrainingOnHandler().get_state().setting_value == 'true'

    if motivation_enabled and training_on:
        coach_name = SystemMotivationCoachHandler().get_state().setting_value

        handler = MotivationHandlerFactory(config.motivation).get_handler()

        handler.say_motivate(coach_name)


Instrumentator().instrument(app).expose(app)
