from fastapi import APIRouter

from trainr.backend.api.v1.model.system import SystemSettingInfoApiModel
from trainr.backend.api.v1.model.system import SystemSettingInputApiModel
from trainr.backend.handler.model.system.settings import \
    SystemSettingsHandlerModel
from trainr.backend.handler.system.last_seconds import SystemLastSecondsHandler
from trainr.backend.handler.system.mode import SystemModeHandler
from trainr.backend.handler.system.reading_type import SystemReadingTypeHandler
from trainr.backend.handler.system.user_name import SystemUserNameHandler


def get_router(handler: SystemSettingsHandlerModel):
    tags = [handler.setting_name]

    router = APIRouter(
        prefix=f'/{handler.setting_name}',
        tags=tags
    )

    @router.get('/', tags=tags, response_model=SystemSettingInfoApiModel, summary=f'Get {handler.setting_name} setting value.')
    async def get_state() -> SystemSettingInfoApiModel:
        data = handler.get_state()

        return SystemSettingInfoApiModel(setting_value=data.setting_value, setting_name=handler.setting_name)

    @router.put('/', tags=tags, summary=f'Register {handler.setting_name} setting value.')
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
user_name_router = get_router(SystemUserNameHandler())

router.include_router(mode_router)
router.include_router(reading_type_router)
router.include_router(last_seconds_router)
router.include_router(user_name_router)
