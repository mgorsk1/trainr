from abc import ABC
from abc import abstractmethod

from trainr.backend.handler.model.fan import FanStateHandlerModel


class FanHandler(ABC):
    def __init__(self, config, **kwargs):
        self.state = None
        self.config = config

    @property
    @abstractmethod
    def speed_min(self) -> int:
        pass

    @property
    @abstractmethod
    def speed_max(self) -> int:
        pass

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def _decrease_speed(self):
        pass

    @abstractmethod
    def _increase_speed(self):
        pass

    @abstractmethod
    def get_state(self) -> FanStateHandlerModel:
        pass

    def set_speed(self, level: int):
        if not self.state:
            self.get_state()

        if not self.state.is_on:
            self.turn_on()

        start_state = self.state.speed
        if self.speed_max >= level >= self.speed_min:
            if level > self.state.speed:
                for _ in range(level - start_state):
                    self._increase_speed()
            if level < self.get_state().speed:
                for _ in range(start_state - level):
                    self._decrease_speed()
