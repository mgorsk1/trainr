from trainr.backend.handler.system import SystemHandler
from trainr.utils import ReadingType


class SystemReadingTypeHandler(SystemHandler):
    @property
    def setting_name(self):
        return 'reading_type'

    @property
    def setting_default_value(self):
        return ReadingType.HR
