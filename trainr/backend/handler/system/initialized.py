from trainr.backend.handler.system import SystemSettingHandler


class SystemInitializedHandler(SystemSettingHandler):
    @property
    def setting_name(self):
        return 'initialized'

    @property
    def setting_default_value(self):
        return 'false'
