from trainr.backend.handler.system import SystemSettingHandler
from trainr.utils import ReadingType


class SystemReadingTypeHandler(SystemSettingHandler):
    @property
    def setting_name(self):
        return 'reading_type'

    @property
    def setting_default_value(self):
        return ReadingType.HR
