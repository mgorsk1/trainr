from abc import ABC, abstractmethod
import random
from importlib import import_module
from typing import List


class MotivationHandler(ABC):
    def __init__(self, config, **kwargs):
        self.config = config

    @abstractmethod
    def say(self, coach: str):
        pass

    def get_quotes(self, coach: str) -> List[str]:
        try:
            m = import_module(f'trainr.backend.handler.motivation.quotes.{coach}')

            quotes = getattr(m, 'quotes')

            return quotes
        except Exception:
            raise NotImplementedError(f'Coach {self.coach} not supported!')

    def get_quote(self, coach: str) -> str:
        return random.choice(self.get_quotes(coach))
