from fastapi import APIRouter

from trainr.api.v1.model.system import SystemSettingInfoApiModel, SystemSettingInputApiModel
from trainr.handler.model.system.settings import SystemSettingsHandlerModel
from trainr.handler.system.last_seconds import SystemLastSecondsHandler
from trainr.handler.system.mode import SystemModeHandler
from trainr.handler.system.reading_type import SystemReadingTypeHandler


def get_router(handler: SystemSettingsHandlerModel):
    router = APIRouter(
        prefix=f'/{handler.setting_name}',
        tags=['system']
    )

    @router.get('/', tags=['system'], response_model=SystemSettingInfoApiModel)
    async def get_state() -> SystemSettingInfoApiModel:
        data = handler.get_state()

        return SystemSettingInfoApiModel(setting_value=data.setting_value, setting_name=handler.setting_name)

    @router.put('/', tags=['system'])
    async def set_value(mode: SystemSettingInputApiModel) -> SystemSettingInfoApiModel:
        handler.set_mode(mode.setting_value)

        data = handler.get_state()

        return SystemSettingInfoApiModel(setting_value=data.setting_value, setting_name=handler.setting_name)

    return router


router = APIRouter(
    prefix='/system',
    tags=['system']
)

mode_router = get_router(SystemModeHandler())
reading_type_router = get_router(SystemReadingTypeHandler())
last_seconds_router = get_router(SystemLastSecondsHandler())

router.include_router(mode_router)
router.include_router(reading_type_router)
router.include_router(last_seconds_router)
