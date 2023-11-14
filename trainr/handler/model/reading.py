from dataclasses import dataclass

from datalite import datalite


@datalite(db_path='trainr.db')
@dataclass
class ReadingZoneHandlerModel:
    zone: int
    range_from: int
    range_to: int
    display_name: str
    reading_type: str


@datalite(db_path='trainr.db')
@dataclass
class ReadingZoneSpecHandlerModel(ReadingZoneHandlerModel):
    pass


@datalite(db_path='trainr.db')
@dataclass
class ThresholdHandlerModel:
    reading_value: int
    reading_type: str


@datalite(db_path='trainr.db')
@dataclass
class ReadingHandlerModel:
    time: int
    reading_value: int
    reading_type: int
