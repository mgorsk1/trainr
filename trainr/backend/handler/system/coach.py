from trainr.backend.handler.system import SystemSettingHandler


class SystemMotivationHandler(SystemSettingHandler):
    @property
    def setting_name(self):
        return 'motivation_enabled'

    @property
    def setting_default_value(self):
        return 'false'


class SystemMotivationCoachHandler(SystemSettingHandler):
    @property
    def setting_name(self):
        return 'motivation_coach'

    @property
    def setting_default_value(self):
        return 'snoop_dogg'
