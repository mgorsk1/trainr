from fastapi import APIRouter

from trainr.backend.api.v1.model.health import HealthApiModel

router = APIRouter(
    prefix='/health',
    tags=['health']
)


@router.get('/', response_model=HealthApiModel)
async def get_health():
    return HealthApiModel(healthy=True)
