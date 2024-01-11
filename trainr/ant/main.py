import time

import click

from trainr.ant.logger import logger
from trainr.ant.publisher.factory import AntPublisherFactory


@click.command()
@click.option('--publish-interval', default=5, help='Interval (in seconds) between consecutive publish operations.')
@click.option('--device-id', default=0, help='ID of ANT+ device. Run "openant scan" to find out what is ID of your device.')
@click.option('--backend-url', default='http://localhost:8080', help='Url for backend to post readings.')
def run(publish_interval: int, device_id: int, backend_url: str):
    factory = AntPublisherFactory
    factory.api_url = backend_url

    publisher = AntPublisherFactory.get_publisher(
        device_id, backend_url=backend_url)

    publisher.run(publish_interval)


if __name__ == '__main__':
    run()
