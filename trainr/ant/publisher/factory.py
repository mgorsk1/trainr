import os
import sys
import threading
import time

import requests

from trainr.ant.logger import logger
from trainr.ant.publisher.ftp import FTPPublisher
from trainr.ant.publisher.hr import HRPublisher


class ReadingTypeWatcher(threading.Thread):
    def __init__(self, reading_type: str):
        threading.Thread.__init__(self)
        self.reading_type = reading_type

    def run(self):
        while True:
            reading_type = AntPublisherFactory.get_reading_type()

            if self.reading_type != reading_type:
                logger.info(
                    f'Reading type changed from [{self.reading_type}] to [{reading_type}]. Restarting.')

                os.execv(sys.executable, ['python'] + sys.argv)

            time.sleep(10)


class AntPublisherFactory:
    api_url = os.getenv('ANT__BACKEND_API_URL', 'http://localhost:8080')

    @classmethod
    def get_reading_type(cls):
        data = requests.get(
            f'{AntPublisherFactory.api_url}/api/v1/system/reading_type').json()['setting_value']

        return data

    @classmethod
    def get_publisher(cls, device_id: int, **kwargs):
        publisher_type = AntPublisherFactory.get_reading_type()

        if publisher_type == 'HR':
            logger.info('Creating publisher for [HR] reading type.')
            publisher = HRPublisher(device_id, **kwargs)
        elif publisher_type == 'FTP':
            logger.info('Creating publisher for [FTP] reading type.')
            publisher = FTPPublisher(device_id, **kwargs)
        else:
            raise NotImplementedError(
                f'Publisher [{publisher_type}] not implemented.')

        ReadingTypeWatcher(publisher_type).start()

        return publisher
