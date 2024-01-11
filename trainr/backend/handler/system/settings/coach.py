from trainr.backend.handler.system import SystemHandler


class SystemMotivationHandler(SystemHandler):
    @property
    def setting_name(self):
        return 'motivation_enabled'

    @property
    def setting_default_value(self):
        return 'false'


class SystemMotivationCoachHandler(SystemHandler):
    @property
    def setting_name(self):
        return 'motivation_coach'

    @property
    def setting_default_value(self):
        return 'snoop_dogg'
