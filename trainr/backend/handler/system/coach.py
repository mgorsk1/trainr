from trainr.backend.handler.system import SystemSettingHandler


class SystemCoachHandler(SystemSettingHandler):
    @property
    def setting_name(self):
        return 'coach'

    @property
    def setting_default_value(self):
        return 'snoop_dogg'

