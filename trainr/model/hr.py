from dataclasses import dataclass

from datalite import datalite


@datalite(db_path="trainr.db")
@dataclass
class HRZone:
    zone: int
    range_from: int
    range_to: int


@datalite(db_path='trainr.db')
@dataclass
class HRReading:
    time: int
    value: int
