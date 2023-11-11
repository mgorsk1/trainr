import os

from fastapi import APIRouter

from trainr.api.v1.models.fan import FanSpeed
from trainr.handler.fan import HBFan
from trainr.utils import fan_speed_mapping

router = APIRouter(
    prefix='/fan',
    tags=['fan']
)

global handler

fan_device_id = os.getenv('FAN_DEVICE_ID')
fan_ip = os.getenv('FAN_IP')
fan_local_key = os.getenv('FAN_LOCAL_KEY')

handler = HBFan(fan_device_id, fan_ip, fan_local_key)


@router.get("/", tags=["fan"])
async def get_state():
    return handler.get_state()


@router.put("/on", tags=["fan"])
async def turn_on():
    handler.turn_on()

    return handler.get_state()


@router.put("/off", tags=["fan"])
async def turn_off():
    handler.turn_off()

    return handler.get_state()


@router.put("/speed/{speed}", tags=["fan"])
async def set_speed(speed: FanSpeed):
    if handler.state.is_on:
        level = fan_speed_mapping.get(speed)

        handler.set_speed(level)

    return handler.get_state()
