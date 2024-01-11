import logging


def get_logger(name='trainr'):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | %(lineno)s | %(message)s')

    # Create a console handler and set the formatter
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)

    return logger


logger = get_logger()
