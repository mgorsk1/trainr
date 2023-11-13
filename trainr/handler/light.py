from huesdk import Hue

from trainr.model.light import LightState
from trainr.utils import light_color_mapping


class HueGroup:
    def __init__(self, hue_bridge_ip: str, user_name: str, group_name: str = 'Salon'):
        self.hue = Hue(bridge_ip=hue_bridge_ip, username=user_name)

        self.group = self.hue.get_group(name=group_name)

    def turn_on(self):
        self.group.on()
        self.group.set_brightness(254, transition=10)

    def turn_off(self):
        self.group.off(transition=10)

    def set_color(self, hue: int, saturation: int):
        self.group.set_color(hue=hue, transition=0)
        self.group.set_saturation(saturation, transition=5)
        self.group.set_brightness(254, transition=5)

    def get_state(self):
        # @todo figure this out properly
        display_name = light_color_mapping.get(self.hue.get_light(name='Komoda').hue, 'N/A')
        return LightState(is_on=self.group.is_on, color=self.group.hue, display_name=display_name)
