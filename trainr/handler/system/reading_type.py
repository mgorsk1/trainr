from trainr.api.v1.model.system.reading_type import ReadingType

from trainr.handler.system import SystemSettingHandler


class SystemReadingTypeHandler(SystemSettingHandler):
    @property
    def setting_name(self):
        return 'reading_type'

    @property
    def setting_default_value(self):
        return ReadingType.HR
