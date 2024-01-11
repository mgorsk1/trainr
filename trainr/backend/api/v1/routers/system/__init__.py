from fastapi import APIRouter

from trainr.backend.api.v1.routers.system.settings import \
    router as settings_router
from trainr.backend.api.v1.routers.system.state import router as state_router

router = APIRouter(
    prefix='/system',
)

router.include_router(settings_router, prefix='/settings',
                      tags=['system settings'])
router.include_router(state_router, prefix='/state', tags=['system state'])
