from fastapi import APIRouter

from trainr.backend.api.v1.model.motivation import MotivationInfoApiModel, MotivationInputApiModel
from trainr.backend.config import config
from trainr.backend.handler.factory import MotivationHandlerFactory

router = APIRouter(
    prefix='/motivation',
    tags=['motivation']
)

global handler

handler = MotivationHandlerFactory(config.motivation).get_handler()


@router.post('/quote', tags=['motivation'], response_model=MotivationInfoApiModel)
async def say_quote(motivation: MotivationInputApiModel) -> MotivationInfoApiModel:
    quote = handler.say(motivation.coach)

    return MotivationInfoApiModel(text=quote, coach=motivation.coach)
