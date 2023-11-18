from fastapi import APIRouter

from trainr.backend.api.v1.routers import fan
from trainr.backend.api.v1.routers import health
from trainr.backend.api.v1.routers import light
from trainr.backend.api.v1.routers import reading
from trainr.backend.api.v1.routers import system

v1 = APIRouter(prefix='/v1')

v1.include_router(health.router)
v1.include_router(fan.router)
v1.include_router(light.router)
v1.include_router(reading.hr_router)
v1.include_router(reading.ftp_router)
v1.include_router(system.router)
