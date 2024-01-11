from trainr.backend.handler.system import SystemHandler


class SystemUserNameHandler(SystemHandler):
    @property
    def setting_name(self):
        return 'user_name'

    @property
    def setting_default_value(self):
        return ''
