
from fastapi import APIRouter

from trainr.api.v1.routers.system.mode import router as mode_router
from trainr.api.v1.routers.system.reading_type import router as reading_type_router

router = APIRouter(
    prefix='/system',
    tags=['system']
)

router.include_router(mode_router)
router.include_router(reading_type_router)
