import os

import reflex as rx

from typing import List, Tuple

from trainr.handler.fan import HBFan
from trainr.handler.hr import HR
from trainr.handler.light import HueGroup
from trainr.utils import fan_speed_display_name_mapping, hr_zones_light_mapping, light_spec_mapping, fan_speed_mapping

global fan_handler
global handler

# Fan ------------------------------------------------------------------------------------------------------------------
fan_device_id = os.getenv('FAN_DEVICE_ID')
fan_ip = os.getenv('FAN_IP')
fan_local_key = os.getenv('FAN_LOCAL_KEY')

fan_handler = HBFan(fan_device_id, fan_ip, fan_local_key)

# Light ----------------------------------------------------------------------------------------------------------------
hue_bridge_ip = os.getenv('HUE_BRIDGE_IP')
hue_bridge_username = os.getenv('HUE_BRIDGE_USERNAME')

light_handler = HueGroup(hue_bridge_ip, hue_bridge_username)

# HR -------------------------------------------------------------------------------------------------------------------
hr_handler = HR()


class State(rx.State):
    reading_value: int = 100
    reading_type: str = 'HR'

    hr_threshold: int
    hr_zones: List[Tuple[int, int, int]]

    fan_on: bool
    fan_speed: int

    light_on: bool
    light_color: str

    @rx.var
    def reading_type_display_name(self):
        return self.reading_type.upper()

    @rx.var
    def fan_speed_name(self) -> str:
        return fan_speed_display_name_mapping.get(self.fan_speed, 'N/A')

    @rx.var
    def fan_speed_caption(self):
        return self.fan_speed_name if self.fan_on else 'OFF'

    @rx.var
    def light_color_caption(self):
        return self.light_color if self.light_on else 'OFF'

    @rx.var
    def reading_percent(self) -> int:
        try:
            return int(100 * self.reading_value / self.hr_zones[-1][2])
        except:
            return 0

    @rx.var
    def zones(self):
        if self.reading_type == 'HR':
            return self.hr_zones
        else:
            return []

    @rx.var
    def active_zone(self) -> int:
        for z in self.zones:
            if self.reading_value >= z[1] and self.reading_value < z[2]:
                return z[0]

        return 0

    @rx.var
    def active_zone_color(self) -> str:
        if self.reading_type == 'HR':
            return hr_zones_light_mapping.get(self.active_zone, 'N/A').name

    def get_data(self):
        self.hr_threshold = hr_handler.get_threshold_hr().hr
        self.hr_zones = [(z.zone, z.range_from, z.range_to) for z in hr_handler.get_hr_zones()]

        fan_state = fan_handler.get_state()

        self.fan_on = fan_state.is_on
        self.fan_speed = fan_state.speed

        light_state = light_handler.get_state()

        self.light_on = light_state.is_on
        self.light_color = light_state.display_name

    def toggle_fan(self, fan_on: bool):
        if self.fan_on:
            fan_handler.turn_off()
        else:
            fan_handler.turn_on()

        self.fan_on = fan_on

    def set_fan_speed(self, fan_speed: str):
        if self.fan_on:
            fan_speed = fan_speed_mapping[fan_speed]
            fan_handler.set_speed(fan_speed)
            self.fan_speed = fan_speed

    def toggle_light(self, light_on: bool):
        if self.light_on:
            light_handler.turn_off()
        else:
            light_handler.turn_on()

        self.light_on = light_on

    def set_light_color(self, light_color: str):
        if self.light_on:
            light_spec = light_spec_mapping[light_color]
            light_handler.set_color(light_spec.hue, light_spec.saturation)

            self.light_color = light_spec.hue

    def set_hr_threshold(self, threshold: int):
        self.hr_threshold = threshold

    def calculate_hr_zones(self):
        hr_handler.set_threshold_hr(self.hr_threshold)

        self.hr_zones = [(z.zone, z.range_from, z.range_to) for z in hr_handler.get_hr_zones()]
