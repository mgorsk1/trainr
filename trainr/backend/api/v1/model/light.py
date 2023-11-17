from dataclasses import dataclass
from enum import Enum


@dataclass
class LightStateApiModel:
    color: str
    is_on: bool
    display_name: str


@dataclass
class LightColorInputApiModel:
    color_name: str


class Color(str, Enum):
    WHITE = 'WHITE'
    NAVY = 'NAVY'
    BLUE = 'BLUE'
    GREEN = 'GREEN'
    YELLOW = 'YELLOW'
    ORANGE = 'ORANGE'
    RED = 'RED'

