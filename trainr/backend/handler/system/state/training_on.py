from trainr.backend.handler.system import SystemHandler


class TrainingOnHandler(SystemHandler):
    @property
    def setting_name(self):
        return 'training_on'

    @property
    def setting_default_value(self):
        return 'false'
