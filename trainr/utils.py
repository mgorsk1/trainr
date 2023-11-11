from dataclasses import dataclass
from typing import Dict


@dataclass
class LightColor:
    hue: int
    saturation: int


fan_speed_mapping = {
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3
}

light_spec_mapping = {
    'GRAY': LightColor(hue=22658, saturation=209),
    'BLUE': LightColor(hue=44133, saturation=254),
    'GREEN': LightColor(hue=22658, saturation=209),
    'YELLOW': LightColor(hue=9532, saturation=207),
    'ORANGE': LightColor(hue=6291, saturation=251),
    'RED': LightColor(hue=21, saturation=254),
}

hr_zones_mapping: Dict[int, LightColor] = {
    0: light_spec_mapping['GRAY'],
    1: light_spec_mapping['BLUE'],
    2: light_spec_mapping['GREEN'],
    3: light_spec_mapping['YELLOW'],
    4: light_spec_mapping['ORANGE'],
    5: light_spec_mapping['RED']
}
