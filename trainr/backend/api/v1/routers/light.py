from fastapi import APIRouter

from trainr.backend.api.v1.model.light import LightColorInputApiModel
from trainr.backend.api.v1.model.light import LightStateApiModel
from trainr.backend.config import config
from trainr.backend.handler.factory import LightHandlerFactory
from trainr.utils import LightColor
from trainr.utils import light_name_to_spec_mapping

router = APIRouter(
    prefix='/light',
    tags=['light']
)

global handler

handler = LightHandlerFactory(config.light).get_handler()


@router.get('/', tags=['light'], response_model=LightStateApiModel)
async def get_light_state() -> LightStateApiModel:
    data = handler.get_state()

    return LightStateApiModel(color=data.color, is_on=data.is_on, display_name=data.display_name)


@router.put('/on', tags=['light'], response_model=LightStateApiModel)
async def turn_light_on() -> LightStateApiModel:
    handler.turn_on()

    data = handler.get_state()

    return LightStateApiModel(color=data.color, is_on=data.is_on, display_name=data.display_name)


@router.put('/off', tags=['light'], response_model=LightStateApiModel)
async def turn_light_off() -> LightStateApiModel:
    handler.turn_off()

    data = handler.get_state()

    return LightStateApiModel(color=data.color, is_on=data.is_on, display_name=data.display_name)


@router.put('/color', tags=['light'], response_model=LightStateApiModel)
async def set_light_color(color: LightColorInputApiModel) -> LightStateApiModel:
    color_spec: LightColor = light_name_to_spec_mapping.get(color.color_name)
    handler.set_color(hue=color_spec.hue, saturation=color_spec.saturation)

    data = handler.get_state()

    return LightStateApiModel(color=data.color, is_on=data.is_on, display_name=data.display_name)
