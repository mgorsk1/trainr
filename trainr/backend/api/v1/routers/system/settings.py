from fastapi import APIRouter

from trainr.backend.api.v1.model.system import SystemSettingInfoApiModel
from trainr.backend.api.v1.model.system import SystemSettingInputApiModel
from trainr.backend.handler.system import SystemHandler
from trainr.backend.handler.system.settings.coach import \
    SystemMotivationCoachHandler
from trainr.backend.handler.system.settings.coach import \
    SystemMotivationHandler
from trainr.backend.handler.system.settings.initialized import \
    SystemInitializedHandler
from trainr.backend.handler.system.settings.last_seconds import \
    SystemLastSecondsHandler
from trainr.backend.handler.system.settings.mode import SystemModeHandler
from trainr.backend.handler.system.settings.reading_type import \
    SystemReadingTypeHandler
from trainr.backend.handler.system.settings.user_name import \
    SystemUserNameHandler


def get_router(handler: SystemHandler):
    router = APIRouter(
        prefix=f'/{handler.setting_name}'
    )

    @router.get('/', response_model=SystemSettingInfoApiModel, summary=f'Get {handler.setting_name} setting value.')
    async def get_state() -> SystemSettingInfoApiModel:
        data = handler.get_state()

        return SystemSettingInfoApiModel(setting_value=data.setting_value, setting_name=handler.setting_name)

    @router.put('/', summary=f'Register {handler.setting_name} setting value.')
    async def set_value(setting: SystemSettingInputApiModel) -> SystemSettingInfoApiModel:
        handler.set_value(setting.setting_value)

        data = handler.get_state()

        return SystemSettingInfoApiModel(setting_value=data.setting_value, setting_name=handler.setting_name)

    return router


router = APIRouter(
    tags=['system']
)

mode_router = get_router(SystemModeHandler())
reading_type_router = get_router(SystemReadingTypeHandler())
last_seconds_router = get_router(SystemLastSecondsHandler())
user_name_router = get_router(SystemUserNameHandler())
system_initialized_router = get_router(SystemInitializedHandler())
motivation_handler = get_router(SystemMotivationCoachHandler())
motivation_coach_handler = get_router(SystemMotivationHandler())

router.include_router(mode_router)
router.include_router(reading_type_router)
router.include_router(last_seconds_router)
router.include_router(user_name_router)
router.include_router(system_initialized_router)
router.include_router(motivation_handler)
router.include_router(motivation_coach_handler)
