import json
from functools import wraps

import tinytuya
from datalite.fetch import fetch_from

from trainr.models.fan import FanState


def update_fan_state(f):
    @wraps(f)
    def wrapped(self, *args, **kwargs):
        result = f(self, *args, **kwargs)

        self.state.update_entry()

        return result

    return wrapped


class HBFan:
    def __init__(self, device_id: str, ip: str, local_key: str):
        self.device = tinytuya.OutletDevice(device_id, ip, local_key)
        self.device.set_version(3.3)

        try:
            self.state = fetch_from(FanState, 1)
        except KeyError:
            self.state = FanState(speed=1, is_on=False)
            self.state.create_entry()

        self.speed_max = 3
        self.speed_min = 1

    def _run_command(self, command: dict):
        payload = self.device.generate_payload(tinytuya.CONTROL, {"201": json.dumps(command)})

        self.device.send(payload)

    def _press_speed_button(self):
        command = {
            "control": "send_ir",
            "head": "010ece00000000000400100030013e011e",
            "key1": "004#000280##000280#0004F0#000100$",
            "type": 0,
            "delay": 300
        }

        self._run_command(command)

    @update_fan_state
    def _increase_speed(self):
        if self.state.speed == self.speed_max:
            pass
        else:
            self._press_speed_button()
            self.state.speed += 1

    # speed change can only go up so decreasing is actually increasing speed twice
    # from 3 we go to 1 > 2 (press twice)
    # from 2 to 3 > 1 (press twice)
    # for 1 we don't do anything
    @update_fan_state
    def _decrease_speed(self):
        if self.state.speed == self.speed_min:
            pass
        else:
            self._press_speed_button()
            self._press_speed_button()
            self.state.speed -= 1

            self.state.update_entry()

    @update_fan_state
    def turn_off(self):
        command = {
            "control": "send_ir",
            "head": "010ece00000000000400100030013e011e",
            "key1": "004#000280##000280#0005F8#%",
            "type": 0,
            "delay": 300
        }

        self._run_command(command)

        self.state.is_on = False
        self.state.update_entry()

    @update_fan_state
    def turn_on(self):
        if self.state.is_on:
            pass
        else:
            self._press_speed_button()

            self.state.is_on = True
            self.state.update_entry()

    def set_speed(self, level: int):
        start_state = self.state.speed
        if self.speed_max >= level >= self.speed_min:
            if level > self.state.speed:
                for _ in range(level - start_state):
                    self._increase_speed()
            if level < self.state.speed:
                for _ in range(start_state - level):
                    self._decrease_speed()

    def get_state(self):
        return self.state
