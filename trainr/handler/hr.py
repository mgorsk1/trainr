import time
from typing import List, Optional

from trainr.handler.model.hr import HRZoneHandlerModel, HRReadingHandlerModel, ThresholdHRHandlerModel

from datalite.fetch import fetch_equals, fetch_all, fetch_if, fetch_from


class HR:
    def __init__(self):
        self.threshold_hr = 200 if not self.get_threshold_hr() else self.get_threshold_hr().hr

        self.set_threshold_hr(self.threshold_hr)

    def get_hr_reading(self) -> HRReadingHandlerModel:
        return HRReadingHandlerModel(value=120, time=round(time.time() * 1000))

    def save_hr_reading(self, value: int):
        data = HRReadingHandlerModel(value=value, time=round(time.time() * 1000))

        data.create_entry()

        return data

    def get_hr_history(self, minutes: int) -> List[HRReadingHandlerModel]:
        date_from = round(time.time() * 1000) - (minutes * 60 * 1000)

        return list(fetch_if(HRReadingHandlerModel, f'time >= {date_from}', element_count=10000000))

    def get_hr_zones(self) -> List[HRZoneHandlerModel]:
        return list(fetch_all(HRZoneHandlerModel, element_count=10))

    def set_hr_zones(self):
        pass

    def get_hr_zone(self, zone: int) -> Optional[HRZoneHandlerModel]:
        try:
            return fetch_equals(HRZoneHandlerModel, 'zone', zone)
        except TypeError:
            return None

    def get_hr_zone_by_hr(self, hr: int) -> HRZoneHandlerModel:
        zones = self.get_hr_zones()

        for z in zones:
            if z.range_from <= hr < z.range_to:
                return z

    def set_hr_zone(self, spec: HRZoneHandlerModel) -> HRZoneHandlerModel:
        if data := self.get_hr_zone(spec.zone):
            data.zone = spec.zone
            data.range_from = spec.range_from
            data.range_to = spec.range_to

            data.update_entry()

            return data
        else:
            spec.create_entry()

            return spec

    def _set_zones_from_threshold(self):
        for z in self.get_zones_spec():
            try:

                f = int(int(self.threshold_hr) * z.range_from / 100)
                n = int(int(self.threshold_hr) * z.range_to / 100)

                self.set_hr_zone(HRZoneHandlerModel(zone=z.zone, range_from=f + 1, range_to=n, display_name=z.display_name))
            except IndexError:
                pass

    def set_threshold_hr(self, threshold: int):
        try:
            data = fetch_from(ThresholdHRHandlerModel, 1)
            data.hr = threshold
            data.update_entry()
        except:
            data = ThresholdHRHandlerModel(hr=threshold)
            data.create_entry()

        self.threshold_hr = threshold
        self._set_zones_from_threshold()

    def get_threshold_hr(self) -> Optional[ThresholdHRHandlerModel]:
        try:
            return fetch_from(ThresholdHRHandlerModel, 1)
        except:
            return None

    def get_zones_spec(self) -> List[HRZoneHandlerModel]:
        return [
            HRZoneHandlerModel(zone=1, range_from=0, range_to=68, display_name='Active Recovery'),
            HRZoneHandlerModel(zone=2, range_from=68, range_to=83, display_name='Anaerobic Capacity'),
            HRZoneHandlerModel(zone=3, range_from=83, range_to=95, display_name='Tempo'),
            HRZoneHandlerModel(zone=4, range_from=95, range_to=105, display_name='Threshold'),
            HRZoneHandlerModel(zone=5, range_from=105, range_to=200, display_name='VO2 Max'),
        ]
