from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import BackgroundTasks

from trainr.backend.api.v1.model.fan import FanSpeedInputApiModel
from trainr.backend.api.v1.model.light import LightColorInputApiModel
from trainr.backend.api.v1.model.reading import ReadingInfoApiModel
from trainr.backend.api.v1.model.reading import ReadingInputApiModel
from trainr.backend.api.v1.model.reading import ThresholdInfoApiModel
from trainr.backend.api.v1.model.reading import ZoneInfoApiModel
from trainr.backend.api.v1.model.reading import ZoneInputApiModel
from trainr.backend.api.v1.routers.fan import set_fan_speed
from trainr.backend.api.v1.routers.light import set_light_color
from trainr.backend.handler.reading.ftp import FTPReadingHandler
from trainr.backend.handler.reading.hr import HRReadingHandler
from trainr.backend.handler.system.last_seconds import SystemLastSecondsHandler
from trainr.backend.handler.system.mode import SystemModeHandler
from trainr.backend.handler.system.reading_type import SystemReadingTypeHandler
from trainr.utils import ReadingFunction
from trainr.utils import ReadingType
from trainr.utils import ftp_zone_to_fan_speed_mapping
from trainr.utils import ftp_zone_to_light_spec_mapping
from trainr.utils import hr_zone_to_fan_speed_mapping
from trainr.utils import hr_zone_to_light_spec_mapping


def get_router(handler):
    tags = [handler.reading_type.lower()]

    router = APIRouter(
        prefix=f'/{handler.reading_type.lower()}',
        tags=tags
    )

    async def adjust_system():
        system_on = SystemModeHandler().get_state().setting_value == 'AUTO'
        last_seconds = SystemLastSecondsHandler().get_state().setting_value

        reading_avg = await get_current_reading(seconds=int(last_seconds), function=ReadingFunction.AVG)
        reading_avg = reading_avg.reading

        reading_type = SystemReadingTypeHandler().get_state().setting_value

        zone_to_light_spec_mapping = hr_zone_to_light_spec_mapping \
            if reading_type == ReadingType.HR \
            else ftp_zone_to_light_spec_mapping

        zone_to_fan_spec_mapping = hr_zone_to_fan_speed_mapping \
            if reading_type == ReadingType.HR \
            else ftp_zone_to_fan_speed_mapping

        if system_on and reading_avg > 0:
            zone = await get_zones(hr=reading_avg)
            zone = zone[0].zone if zone else None

            if zone:
                if light_color := zone_to_light_spec_mapping.get(zone):
                    await set_light_color(LightColorInputApiModel(color_name=light_color.name.upper()))

                if fan_speed := zone_to_fan_spec_mapping.get(zone):
                    await set_fan_speed(FanSpeedInputApiModel(fan_speed=fan_speed))

    @router.get('/', tags=tags, response_model=ReadingInfoApiModel, summary=f'Get last {handler.reading_type} reading.')
    async def get_current_reading(seconds: int = 10, function: ReadingFunction = ReadingFunction.LAST):
        if function == ReadingFunction.LAST:
            data = handler.get_reading(seconds)
        elif function == ReadingFunction.AVG:
            data = handler.get_reading_avg(seconds)
        else:
            raise NotImplementedError(
                f'Reading function {function} not supported')

        return ReadingInfoApiModel(reading=data.reading_value, time=data.time.strftime('%s'))

    @router.post('/', tags=tags, response_model=ReadingInfoApiModel,
                 summary=f'Register {handler.reading_type} reading.')
    async def set_current_reading(reading: ReadingInputApiModel,
                                  background_tasks: BackgroundTasks) -> ReadingInfoApiModel:
        data = handler.save_reading(reading.reading)

        background_tasks.add_task(adjust_system)

        return ReadingInfoApiModel(reading=data.reading_value, time=data.time.strftime('%s'))

    @router.get('/history', tags=tags, response_model=List[ReadingInfoApiModel],
                summary=f'Get {handler.reading_type} reading history.')
    async def get_reading_history(seconds: int = 10) -> List[ReadingInfoApiModel]:
        data = handler.get_reading_history(seconds)

        return [ReadingInfoApiModel(reading=r.reading_value, time=r.time.strftime('%s')) for r in data]

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

    @router.get('/zone', tags=tags, response_model=Optional[ZoneInfoApiModel],
                summary=f'Get {handler.reading_type} zone.')
    async def get_zone(zone: int = -1, hr: int = -1) -> Optional[ZoneInfoApiModel]:
        if zone > 0:
            data = handler.get_reading_zone(zone)
        elif hr >= 0:
            data = handler.get_reading_zone_by_reading(hr)
        else:
            return None

        if data:
            return ZoneInfoApiModel(zone=data.zone,
                                    range_from=data.range_from,
                                    range_to=data.range_to,
                                    display_name=data.display_name)
        else:
            return None

    @router.put('/zone', tags=tags, response_model=ZoneInfoApiModel, summary=f'Register {handler.reading_type} zone.')
    async def set_zone_info(zone_info: ZoneInputApiModel):
        hr_zone_spec = ZoneInfoApiModel(
            zone=zone_info.zone, range_from=zone_info.range_from, range_to=zone_info.range_to)

        data = handler.set_reading_zone(hr_zone_spec)

        return ZoneInfoApiModel(zone=data.zone, range_from=data.range_from, range_to=data.range_to)

    @router.get('/threshold', tags=tags, response_model=ThresholdInfoApiModel,
                summary=f'Get {handler.reading_type} threshold.')
    async def get_threshold():
        data = handler.get_threshold()

        return ThresholdInfoApiModel(threshold=data.reading_value if data else 0)

    @router.put('/threshold', tags=tags, response_model=ThresholdInfoApiModel,
                summary=f'Register {handler.reading_type} threshold.')
    async def set_threshold(threshold: ThresholdInfoApiModel):
        handler.set_threshold(threshold.threshold)

        data = handler.get_threshold()

        return ThresholdInfoApiModel(threshold=data.reading_value)

    return router


hr_router = get_router(HRReadingHandler())
ftp_router = get_router(FTPReadingHandler())
