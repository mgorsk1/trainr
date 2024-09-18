from typing import Any

from openant.devices.heart_rate import HeartRate
from openant.devices.heart_rate import HeartRateData

from trainr.ant.publisher import AntPublisher


class HRPublisher(AntPublisher):
    @property
    def reading_type(self) -> str:
        return 'hr'

    @property
    def ant_classes(self):
        return HeartRate, HeartRateData

    def get_reading_from_data(self, data: Any) -> int:
        return int(data.heart_rate)
