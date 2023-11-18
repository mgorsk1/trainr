from huesdk import Hue

from trainr.backend.handler.light.base import LightHandler
from trainr.backend.handler.model.light import LightStateHandlerModel
from trainr.utils import light_color_mapping


class HueGroup(LightHandler):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        self.hue = Hue(bridge_ip=self.config.hue_bridge_ip,
                       username=self.config.hue_bridge_username)

        self.group = self.hue.get_group(name=self.config.hue_bridge_group_name)

    def turn_on(self):
        self.group.on()
        self.group.set_brightness(254, transition=10)

    def turn_off(self):
        self.group.off(transition=10)

    def set_color(self, hue: int, saturation: int):
        if not self.group.is_on:
            self.turn_on()

        self.group.set_color(hue=hue, transition=0)
        self.group.set_saturation(saturation, transition=5)
        self.group.set_brightness(254, transition=5)

    def get_state(self) -> LightStateHandlerModel:
        # @todo figure this out properly
        display_name = light_color_mapping.get(
            self.hue.get_light(name='Komoda').hue, 'N/A')

        return LightStateHandlerModel(is_on=self.group.is_on, color=self.group.hue, display_name=display_name)
