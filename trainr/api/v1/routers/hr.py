from typing import List

from fastapi import APIRouter

from fastapi import BackgroundTasks
from trainr.api.v1.model.fan import FanSpeedInputApiModel
from trainr.api.v1.model.hr import HRReadingInfoApiModel, HRZoneInfoApiModel, HRThresholdInfoApiModel, \
    HRZoneInputApiModel
from trainr.api.v1.model.light import LightColorInputApiModel
from trainr.api.v1.routers.fan import set_fan_speed, turn_fan_off
from trainr.api.v1.routers.light import set_light_color, turn_light_off
from trainr.api.v1.routers.system.mode import get_mode_state
from trainr.handler.hr import HR
from trainr.handler.model.hr import ThresholdHRHandlerModel
from trainr.utils import hr_zone_to_light_spec_mapping, hr_zone_to_fan_speed_mapping

router = APIRouter(
    prefix='/hr',
    tags=['hr']
)

global handler

handler = HR()


# @todo this method should act based on avg from last N seconds not just single reading
async def adjust_system(reading: int):
    system_mode = await get_mode_state()

    system_on = system_mode.system_mode == 'AUTO'

    if system_on:
        if reading > 0:
            zone = await get_hr_zones(hr=reading)
            zone = zone[0].zone

            if light_color := hr_zone_to_light_spec_mapping.get(zone):
                print(light_color)
                await set_light_color(LightColorInputApiModel(color_name=light_color.name.upper()))

            if fan_speed := hr_zone_to_fan_speed_mapping.get(zone):
                print(fan_speed)
                await set_fan_speed(FanSpeedInputApiModel(fan_speed=fan_speed))
        else:
            await turn_fan_off()
            await turn_light_off()


@router.get('/', tags=['hr'], response_model=HRReadingInfoApiModel)
async def get_current_hr():
    data = handler.get_hr_reading()

    return HRReadingInfoApiModel(reading=data.value, time=data.time)


@router.post('/', tags=['hr'], response_model=HRReadingInfoApiModel)
async def set_current_hr(reading: HRReadingInfoApiModel, background_tasks: BackgroundTasks) -> HRReadingInfoApiModel:
    data = handler.save_hr_reading(reading.reading)

    background_tasks.add_task(adjust_system, reading.reading)

    return HRReadingInfoApiModel(reading=data.value, time=data.time)


@router.get('/history', tags=['hr'])
async def get_hr_history(minutes: int = 60):
    data = handler.get_hr_history(minutes)

    return [HRReadingInfoApiModel(reading=r.value, time=r.time) for r in data]


@router.get('/zones', tags=['hr'], response_model=List[HRZoneInfoApiModel])
async def get_hr_zones(zone: int = -1, hr: int = -1) -> List[HRZoneInfoApiModel]:
    if zone > 0:
        data = handler.get_hr_zone(zone)
        return [data] if data else []
    elif hr >= 0:
        data = handler.get_hr_zone_by_hr(hr)

        return [data] if data else []
    else:
        data = handler.get_hr_zones()

        return [HRZoneInfoApiModel(zone=r.zone,
                                   range_from=r.range_from,
                                   range_to=r.range_to,
                                   display_name=r.display_name)
                for r in data]


@router.put('/zones', tags=['hr'], response_model=HRZoneInfoApiModel)
async def set_hr_zone_info(zone_info: HRZoneInputApiModel):
    hr_zone_spec = HRZoneInfoApiModel(
        zone=zone_info.zone, range_from=zone_info.range_from, range_to=zone_info.range_to)

    data = handler.set_hr_zone(hr_zone_spec)

    return HRZoneInfoApiModel(zone=data.zone, range_from=data.range_from, range_to=data.range_to)


@router.get('/threshold', tags=['hr'], response_model=HRThresholdInfoApiModel)
async def get_threshold_hr():
    data: ThresholdHRHandlerModel = handler.get_threshold_hr()

    return HRThresholdInfoApiModel(threshold=data.hr if data else -1)


@router.put('/threshold', tags=['hr'], response_model=HRThresholdInfoApiModel)
async def get_threshold_hr(threshold_hr: HRThresholdInfoApiModel):
    handler.set_threshold_hr(threshold_hr.threshold)

    data: ThresholdHRHandlerModel = handler.get_threshold_hr()

    return HRThresholdInfoApiModel(threshold=data.hr)
