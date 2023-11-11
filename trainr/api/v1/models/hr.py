from dataclasses import dataclass
from typing import List


@dataclass
class HRZoneInfo:
    zone: int
    range_from: int
    range_to: int


@dataclass
class HRZoneInfoPut(HRZoneInfo):
    operation: str

@dataclass
class HRZones:
    zones: List[HRZoneInfo]


@dataclass
class HRReading:
    value: int
    time: int
