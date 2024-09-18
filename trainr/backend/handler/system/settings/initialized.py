from trainr.backend.handler.system import SystemHandler


class SystemInitializedHandler(SystemHandler):
    @property
    def setting_name(self):
        return 'initialized'

    @property
    def setting_default_value(self):
        return 'false'
