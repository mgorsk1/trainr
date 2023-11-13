import os

from fastapi import APIRouter

from trainr.api.v1.models.system.mode import SystemModeInfo
from trainr.handler.system.mode import SystemModeHandler

router = APIRouter(
    prefix='/mode',
    tags=['system']
)

global handler

handler = SystemModeHandler()


@router.get("/", tags=["system"], response_model=SystemModeInfo)
async def get_mode_state():
    data = handler.get_state()

    return SystemModeInfo(value=data.value)


@router.put("/", tags=["system"])
async def set_mode(mode: SystemModeInfo):
    handler.set_mode(mode.value)

    return handler.get_state()
