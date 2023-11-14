import time
from abc import ABC, abstractmethod
from typing import List, Optional

from trainr.handler.model.reading import ReadingZoneHandlerModel, ReadingHandlerModel, ThresholdHandlerModel

from datalite.fetch import fetch_if, fetch_from


class ReadingHandler(ABC):
    def __init__(self):
        self.threshold = 200 if not self.get_threshold(
        ) else self.get_threshold().reading_value

        self.set_threshold(self.threshold)

    @property
    @abstractmethod
    def reading_type(self):
        pass

    def get_reading(self) -> ReadingHandlerModel:
        try:
            data = fetch_if(
                ReadingHandlerModel, f'reading_type=="{self.reading_type}"', page=0, element_count=1)
            return data[-1]
        except IndexError:
            return ReadingHandlerModel(reading_value=-1, reading_type=self.reading_type, time=time.time())

    def save_reading(self, value: int):
        data = ReadingHandlerModel(reading_value=value,
                                   reading_type=self.reading_type,
                                   time=round(time.time() * 1000))

        data.create_entry()

        return data

    def get_reading_history(self, seconds: int) -> List[ReadingHandlerModel]:
        date_from = round(time.time() * 1000) - (seconds * 1000)

        return list(
            fetch_if(ReadingHandlerModel, f'time >= {date_from} and reading_type = "{self.reading_type}"', page=0))

    def get_reading_zones(self) -> List[ReadingZoneHandlerModel]:
        return list(fetch_if(ReadingZoneHandlerModel, f'reading_type=="{self.reading_type}"', page=0))

    def get_reading_zone(self, zone: int) -> Optional[ReadingZoneHandlerModel]:
        try:
            return fetch_if(ReadingZoneHandlerModel, f'reading_type=="{self.reading_type}" and zone=="{zone}"', page=0)[0]
        except TypeError:
            return None

    def get_reading_zone_by_reading(self, reading: int) -> Optional[ReadingZoneHandlerModel]:
        zones = self.get_reading_zones()

        for z in zones:
            if z.range_from <= reading < z.range_to:
                return z

        return None

    def set_reading_zone(self, spec: ReadingZoneHandlerModel) -> ReadingZoneHandlerModel:
        if data := self.get_reading_zone(spec.zone):
            data.zone = spec.zone
            data.range_from = spec.range_from
            data.range_to = spec.range_to

            data.update_entry()

            return data
        else:
            spec.create_entry()

            return spec

    def _set_zones_from_threshold(self):
        for z in self.zones_spec:
            try:

                f = int(int(self.threshold) * z.range_from / 100)
                n = int(int(self.threshold) * z.range_to / 100)

                self.set_reading_zone(ReadingZoneHandlerModel(
                    zone=z.zone,
                    range_from=f + 1,
                    range_to=n,
                    display_name=z.display_name,
                    reading_type=self.reading_type))
            except IndexError:
                pass

    def set_threshold(self, threshold: int):
        try:
            data = self.get_threshold()
            data.reading_value = threshold
            data.update_entry()
        except:
            data = ThresholdHandlerModel(reading_value=threshold,
                                         reading_type=self.reading_type)
            data.create_entry()

        self.threshold = threshold
        self._set_zones_from_threshold()

    def get_threshold(self) -> Optional[ThresholdHandlerModel]:
        try:
            return fetch_if(ThresholdHandlerModel, f'reading_type=="{self.reading_type}"', page=0)[0]
        except:
            return None

    @property
    # @todo specify per reading type
    def zones_spec(self) -> List[ReadingZoneHandlerModel]:
        return [
            ReadingZoneHandlerModel(zone=1, range_from=0, range_to=68,
                                    display_name='Active Recovery', reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=2, range_from=68, range_to=83,
                                    display_name='Anaerobic Capacity', reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=3, range_from=83,
                                    range_to=95, display_name='Tempo', reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=4, range_from=95,
                                    range_to=105, display_name='Threshold', reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=5, range_from=105,
                                    range_to=200, display_name='VO2 Max', reading_type=self.reading_type),
        ]
