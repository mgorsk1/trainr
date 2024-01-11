from abc import ABC
from abc import abstractmethod

from trainr.backend.handler.model.light import LightStateHandlerModel


class LightHandler(ABC):
    def __init__(self, config, **kwargs):
        self.config = config

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def set_color(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_state(self) -> LightStateHandlerModel:
        pass
