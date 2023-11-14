from trainr.handler.system import SystemSettingHandler
from trainr.utils import SystemMode


class SystemModeHandler(SystemSettingHandler):
    @property
    def setting_name(self):
        return 'system_mode'

    @property
    def setting_default_value(self):
        return SystemMode.MANUAL
