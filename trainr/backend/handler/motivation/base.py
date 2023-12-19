import random
from abc import ABC
from abc import abstractmethod
from importlib import import_module
from typing import List


class MotivationHandler(ABC):
    def __init__(self, config, **kwargs):
        self.config = config

    @abstractmethod
    def say(self, text: str):
        pass

    def say_motivate(self, coach: str):
        text = self.get_motivate(coach)

        return self.say(text)

    def say_hello(self, coach: str):
        text = self.get_hello(coach)

        return self.say(text)

    def say_goodbye(self, coach: str):
        text = self.get_goodbye(coach)

        return self.say(text)

    def _get_phrases(self, coach: str, phrase_type: str) -> List[str]:
        try:
            m = import_module(
                f'trainr.backend.handler.motivation.quotes.{coach}')

            quotes = getattr(m, phrase_type)

            return quotes
        except Exception:
            raise NotImplementedError(f'Coach {self.coach} not supported!')

    def get_motivate(self, coach: str) -> str:
        return random.choice(self._get_phrases(coach, 'quotes'))

    def get_hello(self, coach: str) -> str:
        return random.choice(self._get_phrases(coach, 'greetings'))

    def get_goodbye(self, coach: str) -> str:
        return random.choice(self._get_phrases(coach, 'goodbyes'))
