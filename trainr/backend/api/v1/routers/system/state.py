from fastapi import APIRouter

from trainr.backend.api.v1.model.system import SystemStateInfoApiModel
from trainr.backend.api.v1.model.system import SystemStateInputApiModel
from trainr.backend.handler.system import SystemHandler
from trainr.backend.handler.system.state.training_on import TrainingOnHandler


def get_router(handler: SystemHandler):
    router = APIRouter(
        prefix=f'/{handler.setting_name}'
    )

    @router.get('/', response_model=SystemStateInfoApiModel, summary=f'Get {handler.setting_name} state value.')
    async def get_state() -> SystemStateInfoApiModel:
        data = handler.get_state()

        return SystemStateInfoApiModel(setting_value=data.setting_value, setting_name=handler.setting_name)

    @router.put('/', summary=f'Register {handler.setting_name} state value.')
    async def set_value(state: SystemStateInputApiModel) -> SystemStateInfoApiModel:
        handler.set_value(state.setting_value)

        data = handler.get_state()

        return SystemStateInfoApiModel(setting_value=data.setting_value, setting_name=handler.setting_name)

    return router


router = APIRouter(
    tags=['system']
)

training_on_router = get_router(TrainingOnHandler())

router.include_router(training_on_router)
