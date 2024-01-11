from trainr.backend.handler.system import SystemHandler
from trainr.utils import SystemMode


class SystemModeHandler(SystemHandler):
    @property
    def setting_name(self):
        return 'mode'

    @property
    def setting_default_value(self):
        return SystemMode.MANUAL
