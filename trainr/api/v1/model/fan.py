from dataclasses import dataclass
from enum import Enum


class FanSpeed(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


@dataclass
class FanSpeedInputApiModel:
    fan_speed: FanSpeed


@dataclass
class FanStateApiModel:
    speed: int
    is_on: bool
    display_name: str