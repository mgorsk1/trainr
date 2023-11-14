import os

from fastapi import APIRouter

from trainr.api.v1.model.system.reading_type import SystemReadingTypeInfoApiModel, SystemReadingTypeInputApiModel
from trainr.handler.system.reading_type import SystemReadingTypeHandler

router = APIRouter(
    prefix='/reading_type',
    tags=['system']
)

global handler

handler = SystemReadingTypeHandler()


@router.get('/', tags=['system'], response_model=SystemReadingTypeInfoApiModel)
async def get_mode_state() -> SystemReadingTypeInfoApiModel:
    data = handler.get_state()

    return SystemReadingTypeInfoApiModel(reading_type=data.value)


@router.put('/', tags=['system'])
async def set_mode(mode: SystemReadingTypeInputApiModel) -> SystemReadingTypeInfoApiModel:
    handler.set_reading_type(mode.reading_type)

    data = handler.get_state()

    return SystemReadingTypeInfoApiModel(reading_type=data.value)
