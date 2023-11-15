from trainr.backend.handler.system import SystemSettingHandler
from trainr.utils import SystemMode


class SystemModeHandler(SystemSettingHandler):
    @property
    def setting_name(self):
        return 'mode'

    @property
    def setting_default_value(self):
        return SystemMode.MANUAL
