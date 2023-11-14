from datalite.fetch import fetch_from

from trainr.api.v1.model.system.reading_type import ReadingType
from trainr.handler.model.system.reading_type import SystemReadingTypeHandlerModel


class SystemReadingTypeHandler:
    def __init__(self):
        try:
            self.state: SystemReadingTypeHandlerModel = fetch_from(SystemReadingTypeHandlerModel, 1)
        except KeyError:
            self.state = SystemReadingTypeHandlerModel(value=ReadingType.HR)
            self.state.create_entry()

    def get_state(self) -> SystemReadingTypeHandlerModel:
        return self.state

    def set_reading_type(self, reading_type: ReadingType):
        self.state.value = reading_type

        self.state.update_entry()
