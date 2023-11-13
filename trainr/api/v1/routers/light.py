import os

from fastapi import APIRouter

from trainr.api.v1.model.light import LightColorInputApiModel, LightStateApiModel
from trainr.handler.light import HueGroup
from trainr.utils import LightColor, light_name_to_spec_mapping

router = APIRouter(
    prefix='/light',
    tags=['light']
)

global handler

hue_bridge_ip = os.getenv('HUE_BRIDGE_IP')
hue_bridge_username = os.getenv('HUE_BRIDGE_USERNAME')

handler = HueGroup(hue_bridge_ip, hue_bridge_username)


@router.get('/', tags=['light'], response_model=LightStateApiModel)
async def get_state() -> LightStateApiModel:
    data = handler.get_state()

    return LightStateApiModel(color=data.color, is_on=data.is_on, display_name=data.display_name)


@router.put('/on', tags=['light'], response_model=LightStateApiModel)
async def turn_on() -> LightStateApiModel:
    handler.turn_on()

    data = handler.get_state()

    return LightStateApiModel(color=data.color, is_on=data.is_on, display_name=data.display_name)


@router.put('/off', tags=['light'], response_model=LightStateApiModel)
async def turn_off() -> LightStateApiModel:
    handler.turn_off()

    data = handler.get_state()

    return LightStateApiModel(color=data.color, is_on=data.is_on, display_name=data.display_name)


@router.put('/color', tags=['light'], response_model=LightStateApiModel)
async def set_color(color: LightColorInputApiModel) -> LightStateApiModel:
    color_spec: LightColor = light_name_to_spec_mapping.get(color.color_name)
    handler.set_color(hue=color_spec.hue, saturation=color_spec.saturation)

    data = handler.get_state()

    return LightStateApiModel(color=data.color, is_on=data.is_on, display_name=data.display_name)
