from openant.devices.power_meter import PowerData
from openant.devices.power_meter import PowerMeter

from trainr.ant.publisher import AntPublisher


class FTPPublisher(AntPublisher):
    @property
    def reading_type(self) -> str:
        return 'ftp'

    @property
    def ant_classes(self):
        return PowerMeter, PowerData
