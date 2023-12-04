import requests

from trainr.backend.handler.motivation.base import MotivationHandler


class SonosMotivation(MotivationHandler):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        self.url = config.url
        self.room = config.room

    def say(self, coach: str) -> str:
        text = self.get_quote(coach)
        requests.get(f'{self.url}/{self.room}/say/{text}')

        return text
