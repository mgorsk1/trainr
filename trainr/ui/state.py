import asyncio
import os

import reflex as rx

from typing import List, Tuple

import requests

from trainr.utils import hr_zone_to_light_spec_mapping, SystemMode

global api_url

api_url = os.getenv('TRAINR_API_URL', 'http://localhost:1337/api/v1')


class State(rx.State):
    system_mode: str
    system_reading_type: str

    reading_value: int = 0
    reading_threshold: int
    reading_zones: List[Tuple[int, int, int]]

    fan_on: bool
    fan_speed: int
    fan_speed_display_name: str

    light_on: bool
    light_color: str

    # System -----------------------------------------------------------------------------------------------------------

    @rx.var
    def system_mode_auto(self) -> bool:
        return True if self.system_mode == SystemMode.AUTO else False

    @rx.var
    def system_mode_manual(self) -> bool:
        return not self.system_mode_auto

    def toggle_system_mode(self, mode_auto: bool):
        if not mode_auto:
            payload = {'setting_value': SystemMode.MANUAL}
        else:
            payload = {'setting_value': SystemMode.AUTO}

        result = requests.put(f'{api_url}/system/mode', json=payload)
        self.system_mode = result.json().get('setting_value', 'N/A')

    def set_reading_type(self, system_reading_type: str):
        result = requests.put(f'{api_url}/system/reading_type', json={'setting_value': system_reading_type.lower()})

        self.system_reading_type = result.json().get('setting_value', 'N/A').upper()

        self.refresh_system_state()
        self.refresh_reading_state()

    def refresh_system_state(self):
        self.system_mode = requests.get(
            f'{api_url}/system/mode/').json().get('setting_value', 'N/A')

        self.system_reading_type = requests.get(
            f'{api_url}/system/reading_type/').json().get('setting_value', 'N/A').upper()

    # Reading ----------------------------------------------------------------------------------------------------------

    @rx.var
    def reading_type_display_name(self):
        return f'{self.system_reading_type.upper()} {self.reading_type_emoji}'

    @rx.var
    def reading_zone_spec(self):
        try:
            return \
                requests.get(f'{api_url}/{self.system_reading_type.lower()}/zones',
                             params=dict(hr=self.reading_value)).json()[
                    0]
        except (KeyError, IndexError):
            return {'zone': -1, 'display_name': 'Zone Unknown'}

    @rx.var
    def reading_zone(self):
        return self.reading_zone_spec.get('zone')

    @rx.var
    def reading_zone_display_name(self):
        return self.reading_zone_spec.get('display_name')

    @rx.var
    def reading_zone_color(self) -> str:
        if self.system_reading_type.lower() == 'hr':
            if result := hr_zone_to_light_spec_mapping.get(self.reading_zone):
                return result.name
            else:
                return 'N/A'

    @rx.var
    def reading_type_emoji(self):
        map = {
            'HR': '❤️',
            'FTP': '⚡'
        }

        return map.get(self.system_reading_type.upper(), 'N/A') if self.reading_value > 0 else ''

    @rx.var
    def reading_percent(self) -> int:
        try:
            return int(100 * self.reading_value / self.reading_threshold)
        except:
            return 0

    def set_threshold(self, threshold: int):
        self.reading_threshold = threshold

    def calculate_zones(self):
        requests.put(f'{api_url}/{self.system_reading_type.lower()}/threshold',
                     json={'threshold': self.reading_threshold})

        self.reading_zones = [(z.get('zone', 'N/A'), z.get('range_from', 'N/A'), z.get('range_to', 'N/A')) for z in
                              requests.get(f'{api_url}/{self.system_reading_type.lower()}/zones').json()]

    def refresh_reading_state(self):
        self.reading_threshold = requests.get(f'{api_url}/{self.system_reading_type.lower()}/threshold').json().get(
            'threshold', 0)

        try:
            self.reading_zones = [(z.get('zone', 'N/A'), z.get('range_from', 'N/A'), z.get('range_to', 'N/A')) for z in
                                  requests.get(f'{api_url}/{self.system_reading_type.lower()}/zones').json()]
        except AttributeError:
            self.reading_zones = []

    # Fan --------------------------------------------------------------------------------------------------------------

    @rx.var
    def fan_speed_caption(self):
        return self.fan_speed_display_name if self.fan_on else 'OFF'

    @rx.var
    def fan_speed_emoji(self):
        return '💨' * self.fan_speed if self.fan_on else ''

    def toggle_fan(self, fan_on: bool):
        if self.fan_on:
            requests.put(f'{api_url}/fan/off')
        else:
            requests.put(f'{api_url}/fan/on')

        self.fan_on = fan_on

    def set_fan_speed(self, fan_speed_display_name: str):
        if self.fan_on:
            requests.put(f'{api_url}/fan/speed',
                         json=dict(fan_speed=fan_speed_display_name))
            self.fan_speed_display_name = fan_speed_display_name

    def refresh_fan_state(self):
        fan_state = requests.get(f'{api_url}/fan').json()

        self.fan_on = fan_state.get('is_on')
        self.fan_speed = fan_state.get('speed', 0)
        self.fan_speed_display_name = fan_state.get('display_name', 'N/A')

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
            requests.put(f'{api_url}/light/color/',
                         json=dict(color_name=light_color))

            self.light_color = light_color

    def refresh_light_state(self):
        light_state = requests.get(f'{api_url}/light').json()

        self.light_on = light_state.get('is_on')
        self.light_color = light_state.get('display_name', 'N/A')

    # ------------------------------------------------------------------------------------------------------------------

    def get_data(self):
        self.refresh_system_state()
        self.refresh_reading_state()
        self.refresh_fan_state()
        self.refresh_light_state()

    @rx.background
    async def collect_readings(self):
        while True:
            async with self:
                # @todo this should take into account last 15 seconds not all history
                self.reading_value = requests.get(
                    f'{api_url}/{self.system_reading_type.lower()}/', params=dict(seconds=10)).json()['reading']

                self.refresh_fan_state()
                self.refresh_light_state()

            await asyncio.sleep(5)
