from fastapi import APIRouter
from trainr.api.v1.routers import fan, light, hr, system

v1 = APIRouter(prefix='/v1')

v1.include_router(fan.router)
v1.include_router(light.router)
v1.include_router(hr.router)
v1.include_router(system.router)