import asyncio
import os
from typing import List
from typing import Tuple

import reflex as rx
import requests
from requests.exceptions import ConnectionError

from trainr.utils import SystemMode
from trainr.utils import ftp_zone_to_light_spec_mapping
from trainr.utils import hr_zone_to_light_spec_mapping

global api_url

api_url = os.getenv('FRONTEND__API_URL', 'http://localhost:8080/api/v1')


class State(rx.State):
    system_mode: str
    system_reading_type: str
    system_last_seconds: int
    system_backend_healthy: bool

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

    @rx.var
    def system_mode_header_color(self) -> str:
        return 'gray' if self.system_mode_auto else 'black'

    def toggle_system_mode(self, mode_auto: bool):
        if not mode_auto:
            payload = {'setting_value': SystemMode.MANUAL}
        else:
            payload = {'setting_value': SystemMode.AUTO}

        result = requests.put(f'{api_url}/system/mode', json=payload)
        self.system_mode = result.json().get('setting_value', 'N/A')

    def set_reading_type(self, system_reading_type: str):
        result = requests.put(f'{api_url}/system/reading_type',
                              json={'setting_value': system_reading_type})

        self.system_reading_type = result.json().get('setting_value', 'N/A').upper()

        self.refresh_system_state()
        self.refresh_reading_state()

    def set_last_seconds(self, system_last_seconds: int):
        result = requests.put(f'{api_url}/system/last_seconds',
                              json={'setting_value': str(system_last_seconds)})

        self.system_last_seconds = int(result.json().get('setting_value', 0))

        self.refresh_system_state()

    def refresh_system_state(self):
        try:
            self.system_mode = requests.get(
                f'{api_url}/system/mode/').json().get('setting_value', 'N/A')
        except:
            self.system_mode = SystemMode.MANUAL

        try:
            self.system_reading_type = requests.get(
                f'{api_url}/system/reading_type/').json().get('setting_value', 'N/A').upper()
        except:
            self.system_reading_type = 'unknown'

        try:
            self.system_last_seconds = int(requests.get(
                f'{api_url}/system/last_seconds/').json().get('setting_value', 60))
        except:
            self.system_last_seconds = 0

        self.refresh_backend_health()

    def refresh_backend_health(self):
        try:
            backend_healthy = requests.get(f'{api_url}/health').json()['healthy']
        except (ConnectionError, KeyError):
            backend_healthy = False

        self.system_backend_healthy = backend_healthy

    # Reading ----------------------------------------------------------------------------------------------------------

    @rx.var
    def reading_type_display_name(self):
        return f'{self.system_reading_type} {self.reading_type_emoji_active}'

    @rx.var
    def reading_zone_spec(self):
        try:
            return \
                requests.get(f'{api_url}/{self.system_reading_type.lower()}/zones',
                             params=dict(hr=self.reading_value)).json()[
                    0]
        except (AttributeError, KeyError, IndexError, ConnectionError):
            return {'zone': -1, 'display_name': 'Zone Unknown'}

    @rx.var
    def reading_zone(self):
        return self.reading_zone_spec.get('zone')

    @rx.var
    def reading_zone_display_name(self):
        return self.reading_zone_spec.get('display_name')

    @rx.var
    def reading_zone_color(self) -> str:
        if self.system_reading_type == 'HR':
            reading_zone_to_light_spec_mapping = hr_zone_to_light_spec_mapping
        else:
            reading_zone_to_light_spec_mapping = ftp_zone_to_light_spec_mapping

        if result := reading_zone_to_light_spec_mapping.get(self.reading_zone):
            return result.name
        else:
            return 'N/A'

    @rx.var
    def reading_type_emoji(self):
        map = {
            'HR': '❤️',
            'FTP': '⚡'
        }

        return map.get(self.system_reading_type.upper(), 'N/A')

    @rx.var
    def reading_type_emoji_active(self):
        return self.reading_type_emoji if self.reading_value > 0 else ''

    @rx.var
    def reading_percent(self) -> int:
        try:
            return int(100 * self.reading_value / self.reading_threshold)
        except:
            return 0

    def set_threshold(self, threshold: int):
        self.reading_threshold = threshold

        self.calculate_zones()

    def calculate_zones(self):
        requests.put(f'{api_url}/{self.system_reading_type.lower()}/threshold',
                     json={'threshold': self.reading_threshold})

        try:
            self.reading_zones = [(z.get('zone', 'N/A'), z.get('range_from', 'N/A'), z.get('range_to', 'N/A')) for z in
                                  requests.get(f'{api_url}/{self.system_reading_type.lower()}/zones').json()]
        except (AttributeError, ConnectionError):
            self.reading_zones = []

    def refresh_reading_state(self):
        try:
            self.reading_threshold = requests.get(f'{api_url}/{self.system_reading_type.lower()}/threshold').json().get(
                'threshold', 0)

            self.reading_zones = [(z.get('zone', 'N/A'), z.get('range_from', 'N/A'), z.get('range_to', 'N/A')) for z in
                                  requests.get(f'{api_url}/{self.system_reading_type.lower()}/zones').json()]
        except (AttributeError, ConnectionError):
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
        try:
            fan_state = requests.get(f'{api_url}/fan').json()
        except ConnectionError:
            fan_state = {}

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

    @rx.var
    def light_color_class(self):
        map = {
            'NAVY': 'facebook',
            'BLUE': 'twitter',
            'GREEN': 'whatsapp',
            'RED': 'red',
            'YELLOW': 'yellow',
            'WHITE': 'gray',
            'ORANGE': 'orange',
        }

        return map.get(self.light_color, 'gray')

    def refresh_light_state(self):
        try:
            light_state = requests.get(f'{api_url}/light').json()
        except ConnectionError:
            light_state = {}

        self.light_on = light_state.get('is_on', False)
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
                try:
                    self.reading_value = requests.get(
                        f'{api_url}/{self.system_reading_type.lower()}',
                        params=dict(seconds=self.system_last_seconds)).json()['reading']
                except (ConnectionError, KeyError):
                    self.reading_value = 0

                self.refresh_fan_state()
                self.refresh_light_state()
                self.refresh_backend_health()

            await asyncio.sleep(5)
