from datalite.fetch import fetch_from

from trainr.handler.model.system.mode import SystemModeHandlerModel
from trainr.utils import SystemMode


class SystemModeHandler:
    def __init__(self):
        try:
            self.state: SystemModeHandlerModel = fetch_from(SystemModeHandlerModel, 1)
        except KeyError:
            self.state = SystemModeHandlerModel(value=SystemMode.MANUAL)
            self.state.create_entry()

    def get_state(self) -> SystemModeHandlerModel:
        return self.state

    def set_mode(self, mode: SystemMode):
        self.state.value = mode

        self.state.update_entry()
