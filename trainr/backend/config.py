import logging
from os import path

from dotted.collection import DottedDict
from piny import YamlLoader

LOG_FORMAT = '%(asctime)s.%(msecs)03d [%(levelname)s] %(module)s.%(funcName)s:%(lineno)d (%(process)d:' \
    '%(threadName)s) - %(message)s'

LOG_LEVEL = 'INFO'

logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(LOG_LEVEL)

BASE_PATH = path.dirname(__file__)

config = DottedDict(
    YamlLoader(
        path=f'{BASE_PATH}/config/app.yml',
    ).load(),
)
