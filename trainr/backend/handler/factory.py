import importlib
from abc import ABC
from abc import abstractmethod


class HandlerFactory(ABC):
    def __init__(self, config):
        self.config = config

    @property
    @abstractmethod
    def module_name(self):
        pass

    def get_handler(self):
        module = importlib.import_module(self.module_name)
        handler_class = getattr(module, self.config.cls)

        return handler_class(self.config.settings)


class FanHandlerFactory(HandlerFactory):
    @property
    def module_name(self):
        return 'trainr.backend.handler.fan'


class LightHandlerFactory(HandlerFactory):
    @property
    def module_name(self):
        return 'trainr.backend.handler.light'


class MotivationHandlerFactory(HandlerFactory):
    @property
    def module_name(self):
        return 'trainr.backend.handler.motivation'
