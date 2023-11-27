import random

from trainr.ant.publisher import AntPublisher


class HRPublisher(AntPublisher):
    @property
    def reading_type(self) -> str:
        return 'hr'

    def get(self):
        # @todo implement actual
        return random.randrange(90, 180)
