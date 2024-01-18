from typing import List

from trainr.backend.handler.model.reading import ReadingZoneHandlerModel
from trainr.backend.handler.reading import ReadingHandler
from trainr.utils import ReadingType


class FTPReadingHandler(ReadingHandler):  # 0,56,76,91,106,121,10000
    @property
    def reading_type(self):
        return ReadingType.FTP

    @property
    def zones_spec(self) -> List[ReadingZoneHandlerModel]:
        return [
            ReadingZoneHandlerModel(zone=1,
                                    range_from=0,
                                    range_to=60,
                                    display_name='Active Recovery',
                                    reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=2,
                                    range_from=60,
                                    range_to=75,
                                    display_name='Endurance',
                                    reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=3,
                                    range_from=75,
                                    range_to=89,
                                    display_name='Tempo',
                                    reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=4,
                                    range_from=89,
                                    range_to=104,
                                    display_name='Threshold',
                                    reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=5,
                                    range_from=104,
                                    range_to=118,
                                    display_name='VO2 Max',
                                    reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=6,
                                    range_from=118,
                                    range_to=10000,
                                    display_name='Anaerobic Capacity',
                                    reading_type=self.reading_type),
        ]
