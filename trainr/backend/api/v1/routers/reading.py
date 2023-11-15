from typing import List

from fastapi import APIRouter

from fastapi import BackgroundTasks
from trainr.backend.api.v1.model.fan import FanSpeedInputApiModel
from trainr.backend.api.v1.model.reading import ReadingInfoApiModel, ZoneInfoApiModel, ThresholdInfoApiModel, ZoneInputApiModel, \
    ReadingInputApiModel
from trainr.backend.api.v1.model.light import LightColorInputApiModel
from trainr.backend.api.v1.routers.fan import set_fan_speed, turn_fan_off
from trainr.backend.api.v1.routers.light import set_light_color, turn_light_off

from trainr.backend.api.v1.routers.system import mode_router
from trainr.backend.handler.reading.hr import HRReadingHandler
from trainr.backend.handler.reading.ftp import FTPReadingHandler
from trainr.utils import hr_zone_to_light_spec_mapping, hr_zone_to_fan_speed_mapping, ReadingFunction


def get_router(handler):
    tags = [handler.reading_type.lower()]

    router = APIRouter(
        prefix=f'/{handler.reading_type.lower()}',
        tags=tags
    )

    async def adjust_system():
        system_mode = await mode_router.get_mode_state()

        system_on = system_mode.system_mode == 'AUTO'

        history = await get_reading_history()

        if system_on and history:
            reading_avg = int(sum([r.reading for r in history]) / len(history))

            if reading_avg > 0:
                zone = await get_zones(hr=reading_avg)
                zone = zone[0].zone

                if light_color := hr_zone_to_light_spec_mapping.get(zone):
                    await set_light_color(LightColorInputApiModel(color_name=light_color.name.upper()))

                if fan_speed := hr_zone_to_fan_speed_mapping.get(zone):
                    await set_fan_speed(FanSpeedInputApiModel(fan_speed=fan_speed))
            else:
                await turn_fan_off()
                await turn_light_off()

    @router.get('/', tags=tags, response_model=ReadingInfoApiModel)
    async def get_current_reading(seconds: int = 10, function: ReadingFunction = ReadingFunction.LAST):
        if function == ReadingFunction.LAST:
            data = handler.get_reading(seconds)
        elif function == ReadingFunction.AVG:
            data = handler.get_reading_avg(seconds)
        else:
            raise NotImplementedError(
                f'Reading function {function} not supported')

        return ReadingInfoApiModel(reading=data.reading_value, time=data.time.strftime('%s'))

    @router.post('/', tags=tags, response_model=ReadingInfoApiModel)
    async def set_current_reading(reading: ReadingInputApiModel,
                                  background_tasks: BackgroundTasks) -> ReadingInfoApiModel:
        data = handler.save_reading(reading.reading)

        background_tasks.add_task(adjust_system)

        return ReadingInfoApiModel(reading=data.reading_value, time=data.time.strftime('%s'))

    @router.get('/history', tags=tags, response_model=List[ReadingInfoApiModel])
    async def get_reading_history(seconds: int = 10) -> List[ReadingInfoApiModel]:
        data = handler.get_reading_history(seconds)

        return [ReadingInfoApiModel(reading=r.reading_value, time=r.time) for r in data]

    @router.get('/zones', tags=tags, response_model=List[ZoneInfoApiModel])
    async def get_zones(zone: int = -1, hr: int = -1) -> List[ZoneInfoApiModel]:
        if zone > 0:
            data = handler.get_reading_zone(zone)
        elif hr >= 0:
            data = handler.get_reading_zone_by_reading(hr)
        else:
            data = handler.get_reading_zones()

        data = data or []

        data = data if isinstance(data, list) else [data]

        return [ZoneInfoApiModel(zone=r.zone,
                                 range_from=r.range_from,
                                 range_to=r.range_to,
                                 display_name=r.display_name)
                for r in data]

    @router.put('/zones', tags=tags, response_model=ZoneInfoApiModel)
    async def set_zone_info(zone_info: ZoneInputApiModel):
        hr_zone_spec = ZoneInfoApiModel(
            zone=zone_info.zone, range_from=zone_info.range_from, range_to=zone_info.range_to)

        data = handler.set_reading_zone(hr_zone_spec)

        return ZoneInfoApiModel(zone=data.zone, range_from=data.range_from, range_to=data.range_to)

    @router.get('/threshold', tags=tags, response_model=ThresholdInfoApiModel)
    async def get_threshold():
        data = handler.get_threshold()

        return ThresholdInfoApiModel(threshold=data.reading_value if data else 0)

    @router.put('/threshold', tags=tags, response_model=ThresholdInfoApiModel)
    async def get_threshold(threshold: ThresholdInfoApiModel):
        handler.set_threshold(threshold.threshold)

        data = handler.get_threshold()

        return ThresholdInfoApiModel(threshold=data.reading_value)

    return router


hr_router = get_router(HRReadingHandler())
ftp_router = get_router(FTPReadingHandler())
