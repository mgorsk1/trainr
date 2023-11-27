import time

import click

from trainr.ant.logger import logger
from trainr.ant.publisher.factory import AntPublisherFactory


@click.command()
@click.option('--publish-interval', default=10, help='Interval (in seconds) between consecutive publish operations.')
def run(publish_interval: int):
    publisher = AntPublisherFactory.get_publisher()

    while True:
        try:
            publisher.publish(publisher.get())
        except Exception:
            logger.error('Error inside main loop', exc_info=True)

        time.sleep(publish_interval)


if __name__ == '__main__':
    run()
