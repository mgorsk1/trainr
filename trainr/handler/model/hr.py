from dataclasses import dataclass

from datalite import datalite


@datalite(db_path='trainr.db')
@dataclass
class HRZoneHandlerModel:
    zone: int
    range_from: int
    range_to: int
    display_name: str


@datalite(db_path='trainr.db')
@dataclass
class HRZoneSpecHandlerModel(HRZoneHandlerModel):
    pass


@datalite(db_path='trainr.db')
@dataclass
class ThresholdHRHandlerModel:
    hr: int


@datalite(db_path='trainr.db')
@dataclass
class HRReadingHandlerModel:
    time: int
    value: int
