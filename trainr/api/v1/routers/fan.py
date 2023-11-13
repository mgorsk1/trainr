import os

from fastapi import APIRouter

from trainr.api.v1.model.fan import FanSpeedInputApiModel
from trainr.api.v1.model.fan import FanStateApiModel
from trainr.handler.fan import HBFan
from trainr.utils import fan_speed_name_to_int_mapping

router = APIRouter(
    prefix='/fan',
    tags=['fan']
)

global handler

fan_device_id = os.getenv('FAN_DEVICE_ID')
fan_ip = os.getenv('FAN_IP')
fan_local_key = os.getenv('FAN_LOCAL_KEY')

handler = HBFan(fan_device_id, fan_ip, fan_local_key)


@router.get('/', tags=['fan'], response_model=FanStateApiModel)
async def get_state() -> FanStateApiModel:
    state = handler.get_state()

    return FanStateApiModel(is_on=state.is_on, speed=state.speed, display_name=state.display_name)


@router.put('/on', tags=['fan'], response_model=FanStateApiModel)
async def turn_on():
    handler.turn_on()

    state = handler.get_state()

    return FanStateApiModel(is_on=state.is_on, speed=state.speed, display_name=state.display_name)


@router.put('/off', tags=['fan'], response_model=FanStateApiModel)
async def turn_off():
    handler.turn_off()

    state = handler.get_state()

    return FanStateApiModel(is_on=state.is_on, speed=state.speed, display_name=state.display_name)


@router.put('/speed', tags=['fan'], response_model=FanStateApiModel)
async def set_speed(speed: FanSpeedInputApiModel):
    if handler.state.is_on:
        level = fan_speed_name_to_int_mapping.get(speed.fan_speed)

        handler.set_speed(level)

    return handler.get_state()
