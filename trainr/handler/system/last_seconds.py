from trainr.handler.system import SystemSettingHandler


class SystemLastSecondsHandler(SystemSettingHandler):
    @property
    def setting_name(self):
        return 'last_seconds'

    @property
    def setting_default_value(self):
        return 10
