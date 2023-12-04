from abc import ABC, abstractmethod
import random
from typing import List

from trainr.backend.handler.motivation.quotes.morgan_freeman import quotes as morgan_freeman_quotes
from trainr.backend.handler.motivation.quotes.gordon_ramsay import quotes as gordon_ramsay_quotes
from trainr.backend.handler.motivation.quotes.snoop_dogg import quotes as snoop_dogg_quotes


class MotivationHandler(ABC):
    def __init__(self, config, **kwargs):
        self.coach = config.coach

    @abstractmethod
    def say(self, coach: str):
        pass

    @property
    def quotes(self) -> List[str]:
        if self.coach == 'morgan_freeman':
            return morgan_freeman_quotes
        elif self.coach == 'gordon_ramsay':
            return gordon_ramsay_quotes
        elif self.coach == 'snoop_dogg':
            return snoop_dogg_quotes
        else:
            raise NotImplementedError(f'Coach {self.coach} not supported!')

    def get_quote(self) -> str:
        return random.choice(self.quotes)
