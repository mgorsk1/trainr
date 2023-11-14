from dataclasses import dataclass
from typing import List


@dataclass
class ZoneInfoApiModel:
    zone: int
    range_from: int
    range_to: int
    display_name: str


@dataclass
class ZoneInputApiModel(ZoneInfoApiModel):
    pass


@dataclass
class ZonesInfoApiModel:
    zones: List[ZoneInfoApiModel]


@dataclass
class ReadingInputApiModel:
    reading: int


@dataclass
class ReadingInfoApiModel(ReadingInputApiModel):
    time: int


@dataclass
class ThresholdInputApiModel:
    threshold: int


@dataclass
class ThresholdInfoApiModel(ThresholdInputApiModel):
    pass
