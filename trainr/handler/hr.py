import time
from typing import List, Optional, Tuple

from trainr.model.hr import HRZone, HRReading

from datalite.fetch import fetch_equals, fetch_all, fetch_if, fetch_from


class HR:
    def get_hr_reading(self) -> HRReading:
        return HRReading(value=102, time=round(time.time() * 1000))

    def save_hr_reading(self, value: int):
        data = HRReading(value=value, time=round(time.time() * 1000))

        data.create_entry()

        return data

    def get_hr_history(self, minutes: int) -> List[HRReading]:
        date_from = round(time.time() * 1000) - (minutes*60*1000)

        return list(fetch_if(HRReading, f'time >= {date_from}', element_count=10000000))

    def get_hr_zones(self) -> List[HRZone]:
        return list(fetch_all(HRZone, element_count=10))

    def set_hr_zones(self):
        pass

    def get_hr_zone(self, zone: int) -> Optional[HRZone]:
        try:
            return fetch_equals(HRZone, 'zone', zone)
        except TypeError:
            return None

    def set_hr_zone(self, spec: HRZone) -> Tuple[HRZone, str]:
        if data := self.get_hr_zone(spec.zone):
            data.zone = spec.zone
            data.range_from = spec.range_from
            data.range_to = spec.range_to

            data.update_entry()

            return data, 'updated'
        else:
            spec.create_entry()

            return spec, 'created'
