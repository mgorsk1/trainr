
from fastapi import APIRouter

from trainr.api.v1.routers.system.mode import router as mode_router

router = APIRouter(
    prefix='/system',
    tags=['system']
)

router.include_router(mode_router)
