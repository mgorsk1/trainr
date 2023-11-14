from dataclasses import dataclass
from enum import Enum
from typing import Dict


@dataclass
class LightColor:
    hue: int
    saturation: int
    name: str


class SystemMode(str, Enum):
    AUTO = 'AUTO'
    MANUAL = 'MANUAL'


class ReadingFunction(str, Enum):
    LAST = 'last'
    AVG = 'avg'


class ReadingType(str, Enum):
    HR = 'hr'
    FTP = 'ftp'

fan_speed_name_to_int_mapping = {
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3
}

fan_speed_to_display_name_mapping: Dict[int, str] = {
    v: k for k, v in fan_speed_name_to_int_mapping.items()}

light_name_to_spec_mapping = {
    # @todo specify proper gray
    'GRAY': LightColor(hue=22658, saturation=209, name='gray'),
    'BLUE': LightColor(hue=44133, saturation=254, name='blue'),
    'GREEN': LightColor(hue=22658, saturation=209, name='green'),
    'YELLOW': LightColor(hue=9532, saturation=207, name='yellow'),
    'ORANGE': LightColor(hue=6291, saturation=251, name='orange'),
    'RED': LightColor(hue=21, saturation=254, name='red'),
}

light_color_mapping = {v.hue: k for k, v in light_name_to_spec_mapping.items()}

hr_zone_to_light_spec_mapping: Dict[int, LightColor] = {
    0: light_name_to_spec_mapping['GRAY'],
    1: light_name_to_spec_mapping['BLUE'],
    2: light_name_to_spec_mapping['GREEN'],
    3: light_name_to_spec_mapping['YELLOW'],
    4: light_name_to_spec_mapping['ORANGE'],
    5: light_name_to_spec_mapping['RED']
}

hr_zone_to_fan_speed_mapping: Dict[int, str] = {
    1: 'LOW',
    2: 'MEDIUM',
    3: 'MEDIUM',
    4: 'HIGH',
    5: 'HIGH',
}
