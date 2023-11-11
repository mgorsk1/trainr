from typing import Optional

from fastapi import APIRouter

from trainr.api.v1.models.hr import HRReading, HRZoneInfo, HRZoneInfoPut
from trainr.handler.hr import HR
from trainr.model.hr import HRZone

router = APIRouter(
    prefix='/hr',
    tags=['hr']
)

global handler

handler = HR()


@router.get("/", tags=["hr"], response_model=HRReading)
async def get_current_hr():
    data = handler.get_hr_reading()

    return HRReading(value=data.value, time=data.time)


@router.post("/", tags=["hr"], response_model=HRReading)
async def set_current_hr(value: int):
    data = handler.save_hr_reading(value)

    return HRReading(value=data.value, time=data.time)


@router.get("/history", tags=["hr"])
async def get_hr_history(minutes: int = 60):
    data = handler.get_hr_history(minutes)

    return [HRReading(value=r.value, time=r.time) for r in data]


@router.get("/zones", tags=["hr"])
async def get_hr_zones():
    data = handler.get_hr_zones()

    return [HRZoneInfo(zone=r.zone, range_from=r.range_from, range_to=r.range_to) for r in data]


@router.get("/zones/{zone}", tags=["hr"], response_model=Optional[HRZoneInfo])
async def get_hr_zone_info(zone: int):
    data = handler.get_hr_zone(zone)

    return HRZoneInfo(zone=data.zone, range_from=data.range_from, range_to=data.range_to) if data else {}


@router.put('/zones/', tags=["hr"], response_model=HRZoneInfoPut)
async def set_hr_zone_info(zone_info: HRZoneInfo):
    hr_zone_spec = HRZone(zone=zone_info.zone, range_from=zone_info.range_from, range_to=zone_info.range_to)

    data, status = handler.set_hr_zone(hr_zone_spec)

    return HRZoneInfoPut(zone=data.zone, range_from=data.range_from, range_to=data.range_to, operation=status)
