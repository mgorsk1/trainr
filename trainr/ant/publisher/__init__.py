import time
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from typing import Tuple

import requests
from openant.devices import ANTPLUS_NETWORK_KEY
from openant.easy.node import Node

from trainr.ant.logger import logger

global publish_time


class AntPublisher(ABC):
    def __init__(self, device_id: int, **kwargs):
        self.device_id = device_id

        self.api_url = kwargs.get('backend_url', 'http://localhost:8080')
        self.publish_time = datetime.now()

    @property
    @abstractmethod
    def reading_type(self) -> str:
        pass

    @property
    @abstractmethod
    def ant_classes(self) -> Tuple:
        pass

    def run(self, publish_interval: int):
        device_class, device_data_class = self.ant_classes
        node = Node()
        node.set_network_key(0x00, ANTPLUS_NETWORK_KEY)

        def on_found():
            logger.info(f'Device [{device}] found and receiving.')

        def on_device_data(page: int, page_name: str, data):
            if isinstance(data, device_data_class):
                publish_now = datetime.now()
                if (publish_now - self.publish_time).seconds > publish_interval:
                    self._publish(data.heart_rate)
                    self.publish_time = publish_now

        device = device_class(node, device_id=self.device_id)

        device.on_found = on_found
        device.on_device_data = on_device_data

        try:
            node.start()
        except Exception:
            logger.error('Error starting node.', exc_info=True)
        finally:
            device.close_channel()
            node.stop()

    def _publish(self, reading: int):
        try:
            logger.info(f'Publishing [{self.reading_type.upper()}]: {reading}')
            result = requests.post(f'{self.api_url}/api/v1/{self.reading_type.lower()}',
                                   json=dict(reading=reading)).json()
            logger.info(f'API returned: {result}')
            return result
        except Exception:
            logger.warning('Error publishing data.', exc_info=True)
            pass
