import os

from fastapi import APIRouter

from trainr.api.v1.model.system.mode import SystemModeInfoApiModel, SystemModeInputApiModel
from trainr.handler.system.mode import SystemModeHandler

router = APIRouter(
    prefix='/mode',
    tags=['system']
)

global handler

handler = SystemModeHandler()


@router.get('/', tags=['system'], response_model=SystemModeInfoApiModel)
async def get_mode_state():
    data = handler.get_state()

    return SystemModeInfoApiModel(system_mode=data.value)


@router.put('/', tags=['system'])
async def set_mode(mode: SystemModeInputApiModel):
    handler.set_mode(mode.system_mode)

    data = handler.get_state()

    return SystemModeInfoApiModel(system_mode=data.value)
