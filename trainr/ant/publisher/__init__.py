import os
from abc import ABC
from abc import abstractmethod

import requests

from trainr.ant.logger import logger


class AntPublisher(ABC):
    def __init__(self, device_id: int, **kwargs):
        self.device_id = device_id

        self.api_url = os.getenv(
            'ANT__BACKEND_API_URL', 'http://localhost:8080')

    @property
    @abstractmethod
    def reading_type(self) -> str:
        pass

    @abstractmethod
    def get(self):
        pass

    def publish(self, reading: int):
        try:
            logger.info(f'publishing [{self.reading_type.upper()}]: {reading}')
            result = requests.post(f'{self.api_url}/api/v1/{self.reading_type.lower()}',
                                   json=dict(reading=reading)).json()
            logger.info(f'api returned: {result}')
            return result
        except Exception as e:
            raise e
