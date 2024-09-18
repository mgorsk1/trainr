from trainr.backend.handler.system import SystemHandler


class SystemLastSecondsHandler(SystemHandler):
    @property
    def setting_name(self):
        return 'last_seconds'

    @property
    def setting_default_value(self):
        return 10
