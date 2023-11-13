import os

import reflex as rx

from typing import List, Tuple

import requests

from trainr.utils import hr_zones_light_mapping, light_spec_mapping

global api_url

api_url = os.getenv('TRAINR_API_URL', 'http://localhost:1337/api/v1')


class State(rx.State):
    reading_value: int = 125
    reading_type: str = 'hr'
    reading_threshold: int
    reading_zone: str
    reading_zone_display_name: str
    reading_zones: List[Tuple[int, int, int]]

    fan_on: bool
    fan_speed: int
    fan_speed_display_name: str

    light_on: bool
    light_color: str

    # Reading ----------------------------------------------------------------------------------------------------------

    @rx.var
    def reading_type_display_name(self):
        return f'{self.reading_type.upper()} {self.reading_type_emoji}'

    @rx.var
    def reading_zone_color(self) -> str:
        if self.reading_type == 'hr':
            if result := hr_zones_light_mapping.get(self.reading_zone):
                return result.name
            else:
                return 'N/A'

    @rx.var
    def reading_type_emoji(self):
        map = {
            'HR': '❤️',
            'FTP': '⚡'
        }

        return map.get(self.reading_type.upper(), 'N/A') if self.reading_value > 0 else ''

    @rx.var
    def reading_percent(self) -> int:
        try:
            return int(100 * self.reading_value / self.reading_threshold)
        except:
            return 0

    def set_threshold(self, threshold: int):
        self.reading_threshold = threshold

    def calculate_zones(self):
        requests.put(f'{api_url}/{self.reading_type.lower()}/threshold', json={'value': self.reading_threshold})

        self.reading_zones = [(z.get('zone', 'N/A'), z.get('range_from', 'N/A'), z.get('range_to', 'N/A')) for z in
                              requests.get(f'{api_url}/{self.reading_type.lower()}/zones').json()]

    def set_reading_type(self, reading_type: str):
        self.reading_type = reading_type
        self.get_data()

    # Fan --------------------------------------------------------------------------------------------------------------

    @rx.var
    def fan_speed_caption(self):
        return self.fan_speed_display_name if self.fan_on else 'OFF'

    @rx.var
    def fan_speed_emoji(self):
        return "💨" * self.fan_speed

    def toggle_fan(self, fan_on: bool):
        if self.fan_on:
            requests.put(f'{api_url}/fan/off')
        else:
            requests.put(f'{api_url}/fan/on')

        self.fan_on = fan_on

    def set_fan_speed(self, fan_speed_display_name: str):
        if self.fan_on:
            requests.put(f'{api_url}/fan/speed/{fan_speed_display_name}')
            self.fan_speed_display_name = fan_speed_display_name

    # Light ------------------------------------------------------------------------------------------------------------

    @rx.var
    def light_color_caption(self) -> str:
        return self.light_color if self.light_on else 'OFF'

    @rx.var
    def light_on_emoji(self) -> str:
        return '💡' if self.light_on else ''

    def toggle_light(self, light_on: bool):
        if self.light_on:
            requests.put(f'{api_url}/light/off')
        else:
            requests.put(f'{api_url}/light/on')

        self.light_on = light_on

    def set_light_color(self, light_color: str):
        if self.light_on:
            requests.put(f'{api_url}/light/color/{light_color}')

            self.light_color = light_color

    # ------------------------------------------------------------------------------------------------------------------

    def get_data(self):
        try:
            _reading_zone = \
                requests.get(f'{api_url}/{self.reading_type.lower()}/zones', params=dict(hr=self.reading_value)).json()[
                    0]
        except KeyError:
            _reading_zone = {'zone': -1, 'display_name': 'N/A'}

        self.reading_zone = _reading_zone.get('zone')
        self.reading_zone_display_name = _reading_zone.get('display_name')

        self.reading_threshold = requests.get(f'{api_url}/{self.reading_type.lower()}/threshold').json().get('value', 0)

        try:
            self.reading_zones = [(z.get('zone', 'N/A'), z.get('range_from', 'N/A'), z.get('range_to', 'N/A')) for z in
                                  requests.get(f'{api_url}/{self.reading_type.lower()}/zones').json()]
        except AttributeError:
            self.reading_zones = []

        fan_state = requests.get(f'{api_url}/fan').json()

        self.fan_on = fan_state.get('is_on')
        self.fan_speed = fan_state.get('speed', 0)
        self.fan_speed_display_name = fan_state.get('display_name', 'N/A')

        light_state = requests.get(f'{api_url}/light').json()

        self.light_on = light_state.get('is_on')
        self.light_color = light_state.get('display_name', 'N/A')
