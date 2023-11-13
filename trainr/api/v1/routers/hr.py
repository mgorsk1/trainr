from fastapi import APIRouter

from trainr.api.v1.model.hr import HRReadingInfoApiModel, HRZoneInfoApiModel, HRThresholdInfoApiModel, HRZoneInputApiModel
from trainr.handler.hr import HR
from trainr.handler.model.hr import ThresholdHRHandlerModel

router = APIRouter(
    prefix='/hr',
    tags=['hr']
)

global handler

handler = HR()


@router.get("/", tags=["hr"], response_model=HRReadingInfoApiModel)
async def get_current_hr():
    data = handler.get_hr_reading()

    return HRReadingInfoApiModel(reading=data.value, time=data.time)


@router.post("/", tags=["hr"], response_model=HRReadingInfoApiModel)
async def set_current_hr(reading: HRReadingInfoApiModel) -> HRReadingInfoApiModel:
    data = handler.save_hr_reading(reading.hr_reading)

    return HRReadingInfoApiModel(reading=data.value, time=data.time)


@router.get("/history", tags=["hr"])
async def get_hr_history(minutes: int = 60):
    data = handler.get_hr_history(minutes)

    return [HRReadingInfoApiModel(reading=r.value, time=r.time) for r in data]


@router.get("/zones", tags=["hr"])
async def get_hr_zones(zone: int = -1, hr: int = -1):
    if zone > 0:
        data = handler.get_hr_zone(zone)
        return [data]
    elif hr > 0:
        data = handler.get_hr_zone_by_hr(hr)

        return [data]
    else:
        data = handler.get_hr_zones()

        return [HRZoneInfoApiModel(zone=r.zone,
                                   range_from=r.range_from,
                                   range_to=r.range_to,
                                   display_name=r.display_name)
                for r in data]


@router.put('/zones/', tags=["hr"], response_model=HRZoneInfoApiModel)
async def set_hr_zone_info(zone_info: HRZoneInputApiModel):
    hr_zone_spec = HRZoneInfoApiModel(zone=zone_info.zone, range_from=zone_info.range_from, range_to=zone_info.range_to)

    data = handler.set_hr_zone(hr_zone_spec)

    return HRZoneInfoApiModel(zone=data.zone, range_from=data.range_from, range_to=data.range_to)


@router.get('/threshold/', tags=["hr"], response_model=HRThresholdInfoApiModel)
async def get_threshold_hr():
    data: ThresholdHRHandlerModel = handler.get_threshold_hr()

    return HRThresholdInfoApiModel(threshold=data.hr if data else -1)


@router.put('/threshold/', tags=["hr"], response_model=HRThresholdInfoApiModel)
async def get_threshold_hr(threshold_hr: HRThresholdInfoApiModel):
    handler.set_threshold_hr(threshold_hr.threshold)

    data: ThresholdHRHandlerModel = handler.get_threshold_hr()

    return HRThresholdInfoApiModel(threshold=data.hr)
