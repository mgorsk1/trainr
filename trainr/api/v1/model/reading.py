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
class ReadingInfoApiModel:
    reading: int
    time: int


@dataclass
class ReadingInputApiModel(ReadingInfoApiModel):
    pass


@dataclass
class ThresholdInputApiModel:
    threshold: int


@dataclass
class ThresholdInfoApiModel(ThresholdInputApiModel):
    pass
