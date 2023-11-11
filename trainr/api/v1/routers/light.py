import os

from fastapi import APIRouter

from trainr.api.v1.models.light import Color
from trainr.handler.light import HueGroup
from trainr.utils import LightColor, light_spec_mapping

router = APIRouter(
    prefix='/light',
    tags=['light']
)

global handler

hue_bridge_ip = os.getenv('HUE_BRIDGE_IP')
hue_bridge_username = os.getenv('HUE_BRIDGE_USERNAME')

handler = HueGroup(hue_bridge_ip, hue_bridge_username)


@router.get("/", tags=["light"])
async def get_state():
    return handler.get_state()


@router.put("/on", tags=["light"])
async def turn_on():
    handler.turn_on()

    return handler.get_state()


@router.put("/off", tags=["light"])
async def turn_off():
    handler.turn_off()

    return handler.get_state()


@router.put("/color/{color}", tags=["light"])
async def set_color(color: Color):
    color_spec: LightColor = light_spec_mapping.get(color)
    handler.set_color(hue=color_spec.hue, saturation=color_spec.saturation)

    return handler.get_state()
