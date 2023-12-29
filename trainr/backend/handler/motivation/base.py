from abc import ABC
from abc import abstractmethod
from datetime import datetime
from importlib import import_module
from random import Random
from typing import List


class MotivationHandler(ABC):
    def __init__(self, config, **kwargs):
        self.config = config

    @property
    def random(self):
        return Random(datetime.now().timestamp())

    @abstractmethod
    def say(self, text: str, **kwargs):
        pass

    def _say(self, text: str, coach: str):
        voice_id = self.config.coaches[coach].voice_id

        return self.say(text, **dict(voice_id=voice_id))

    def say_motivate(self, coach: str):
        text = self.get_motivate(coach)

        return self._say(text, coach)

    def say_hello(self, coach: str):
        text = self.get_hello(coach)

        return self._say(text, coach)

    def say_goodbye(self, coach: str):
        text = self.get_goodbye(coach)

        return self._say(text, coach)

    def _get_phrases(self, coach: str, phrase_type: str) -> List[str]:
        try:
            m = import_module(
                f'trainr.backend.handler.motivation.quotes.{coach}')

            quotes = getattr(m, phrase_type)

            return quotes
        except Exception:
            raise NotImplementedError(f'Coach {coach} not supported!')

    def get_motivate(self, coach: str) -> str:
        return self.random.choice(self._get_phrases(coach, 'quotes'))

    def get_hello(self, coach: str) -> str:
        return self.random.choice(self._get_phrases(coach, 'greetings'))

    def get_goodbye(self, coach: str) -> str:
        return self.random.choice(self._get_phrases(coach, 'goodbyes'))
