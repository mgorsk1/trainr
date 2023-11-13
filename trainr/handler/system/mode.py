from datalite.fetch import fetch_from

from trainr.model.system.mode import SystemModeState
from trainr.utils import SystemMode


class SystemModeHandler:
    def __init__(self):
        try:
            self.state = fetch_from(SystemModeState, 1)
        except KeyError:
            self.state = SystemModeState(value=SystemMode.MANUAL)
            self.state.create_entry()

    def get_state(self):
        return self.state

    def set_mode(self, mode: SystemMode):
        self.state.value = mode

        self.state.update_entry()