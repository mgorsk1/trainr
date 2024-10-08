import json
from functools import wraps

import tinytuya
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from trainr.backend.handler.database.engine import engine
from trainr.backend.handler.fan.base import FanHandler
from trainr.backend.handler.model.fan import FanStateHandlerModel
from trainr.utils import fan_speed_to_display_name_mapping


def update_fan_state(f):
    @wraps(f)
    def wrapped(self, *args, **kwargs):
        result = f(self, *args, **kwargs)

        with Session(engine, expire_on_commit=False) as session:
            session.add(self.state)

            session.commit()

        return result

    return wrapped


class HBFan(FanHandler):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        self.device = tinytuya.OutletDevice(
            config.hb_device_id, config.hb_fan_ip, config.hb_fan_local_key)
        self.device.set_version(3.3)

    @property
    def speed_min(self) -> int:
        return 1

    @property
    def speed_max(self) -> int:
        return 3

    def _run_command(self, command: dict):
        payload = self.device.generate_payload(
            tinytuya.CONTROL, {'201': json.dumps(command)})

        self.device.send(payload)

    def _press_speed_button(self):
        command = {
            'control': 'send_ir',
            'head': '010ece00000000000400100030013e011e',
            'key1': '004#000280##000280#0004F0#000100$',
            'type': 0,
            'delay': 300
        }

        self._run_command(command)

    @update_fan_state
    def _increase_speed(self):
        if not self.state:
            self.get_state()

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
        if not self.state:
            self.get_state()

        if self.state.speed == self.speed_min:
            pass
        else:
            self._press_speed_button()
            self._press_speed_button()
            self.state.speed -= 1

    @update_fan_state
    def turn_off(self):
        if not self.state:
            self.get_state()

        command = {
            'control': 'send_ir',
            'head': '010ece00000000000400100030013e011e',
            'key1': '004#000280##000280#0005F8#%',
            'type': 0,
            'delay': 300
        }

        self._run_command(command)

        self.state.is_on = False

    @update_fan_state
    def turn_on(self):
        if not self.state:
            self.get_state()

        if self.state.is_on:
            pass
        else:
            self._press_speed_button()

            self.state.is_on = True

    def get_state(self) -> FanStateHandlerModel:
        with Session(engine, expire_on_commit=False) as session:
            try:
                query_statement = select(FanStateHandlerModel)

                self.state = session.scalars(query_statement).one()
            except NoResultFound:
                self.state = FanStateHandlerModel(
                    speed=1, is_on=False, display_name='LOW')

                session.add(self.state)
                session.commit()

        self.state.display_name = fan_speed_to_display_name_mapping.get(
            self.state.speed)

        return self.state
