from fastapi import APIRouter

from trainr.backend.api.v1.model.motivation import MotivationInfoApiModel
from trainr.backend.api.v1.model.motivation import MotivationInputApiModel
from trainr.backend.config import config
from trainr.backend.handler.factory import MotivationHandlerFactory

router = APIRouter(
    prefix='/motivation',
    tags=['motivation']
)

global handler

handler = MotivationHandlerFactory(config.motivation).get_handler()


@router.post('/say/motivate', tags=['motivation'], response_model=MotivationInfoApiModel)
async def say_quote(motivation: MotivationInputApiModel) -> MotivationInfoApiModel:
    quote = handler.say_motivate(motivation.coach)

    return MotivationInfoApiModel(text=quote, coach=motivation.coach, type='motivate')


@router.post('/say/hello', tags=['motivation'], response_model=MotivationInfoApiModel)
async def say_quote(motivation: MotivationInputApiModel) -> MotivationInfoApiModel:
    quote = handler.say_hello(motivation.coach)

    return MotivationInfoApiModel(text=quote, coach=motivation.coach, type='hello')


@router.post('/say/goodbye', tags=['motivation'], response_model=MotivationInfoApiModel)
async def say_quote(motivation: MotivationInputApiModel) -> MotivationInfoApiModel:
    quote = handler.say_goodbye(motivation.coach)

    return MotivationInfoApiModel(text=quote, coach=motivation.coach, type='goodbye')
