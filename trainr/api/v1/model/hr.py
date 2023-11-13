from dataclasses import dataclass
from typing import List


@dataclass
class HRZoneInfoApiModel:
    zone: int
    range_from: int
    range_to: int
    display_name: str


@dataclass
class HRZoneInputApiModel(HRZoneInfoApiModel):
    pass


@dataclass
class HRZonesInfoApiModel:
    zones: List[HRZoneInfoApiModel]


@dataclass
class HRReadingInfoApiModel:
    reading: int
    time: int


@dataclass
class HRReadingInputApiModel(HRReadingInfoApiModel):
    pass


@dataclass
class HRThresholdInputApiModel:
    threshold: int


@dataclass
class HRThresholdInfoApiModel(HRThresholdInputApiModel):
    pass
