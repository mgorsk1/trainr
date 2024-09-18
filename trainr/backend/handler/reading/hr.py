from typing import List

from trainr.backend.handler.model.reading import ReadingZoneHandlerModel
from trainr.backend.handler.reading import ReadingHandler
from trainr.utils import ReadingType


class HRReadingHandler(ReadingHandler):
    @property
    def reading_type(self):
        return ReadingType.HR

    @property
    def zones_spec(self) -> List[ReadingZoneHandlerModel]:
        return [
            ReadingZoneHandlerModel(zone=1,
                                    range_from=0,
                                    range_to=68,
                                    display_name='Active Recovery',
                                    reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=2,
                                    range_from=68,
                                    range_to=83,
                                    display_name='Anaerobic Capacity',
                                    reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=3,
                                    range_from=83,
                                    range_to=95,
                                    display_name='Tempo',
                                    reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=4,
                                    range_from=95,
                                    range_to=105,
                                    display_name='Threshold',
                                    reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=5,
                                    range_from=105,
                                    range_to=200,
                                    display_name='VO2 Max',
                                    reading_type=self.reading_type),
        ]
