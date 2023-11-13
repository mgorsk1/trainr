from dataclasses import dataclass

from datalite import datalite


@datalite(db_path="trainr.db")
@dataclass
class HRZone:
    zone: int
    range_from: int
    range_to: int
    display_name: str


@datalite(db_path="trainr.db")
@dataclass
class HRZoneSpec(HRZone):
    pass


@datalite(db_path="trainr.db")
@dataclass
class ThresholdHR:
    hr: int


@datalite(db_path='trainr.db')
@dataclass
class HRReading:
    time: int
    value: int
