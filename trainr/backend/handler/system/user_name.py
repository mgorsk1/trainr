from trainr.backend.handler.system import SystemSettingHandler


class SystemUserNameHandler(SystemSettingHandler):
    @property
    def setting_name(self):
        return 'user_name'

    @property
    def setting_default_value(self):
        return ''
