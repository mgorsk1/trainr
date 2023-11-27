import random

from trainr.ant.publisher import AntPublisher


class FTPPublisher(AntPublisher):
    @property
    def reading_type(self) -> str:
        return 'ftp'

    def get(self):
        # @todo implement actual
        return random.randrange(100, 210)
