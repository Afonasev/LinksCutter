import logging
import os
import random
import string

import faker

from . import settings
from .domain import Link


def random_str(size, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def fill_fake_links(repository, count):
    factory = faker.Factory.create()

    for _ in range(count):
        repository.save(Link(
            url=factory.url(),
            key=random_str(settings.MIN_KEY_LENGHT),
            created_at=factory.date_time_this_month(),
        ))


def init_logging(path='./logs'):
    _setup_basic_logger_config()

    if not os.path.exists(path):
        os.makedirs(path)

    handlers = []

    for name, level in (
        ('common', logging.INFO),
        ('errors', logging.ERROR),
    ):
        handlers.append(_create_file_handler(path, name, level))

    if settings.DEBUG:
        handlers.append(_create_console_handler())

    root_logger = logging.getLogger()
    root_logger.handlers = handlers


def _setup_basic_logger_config():
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
    )


def _create_file_handler(path, name, level):
    file_path = os.path.join(path, '%s.log' % name)
    handler = logging.FileHandler(file_path)
    handler.setLevel(level)
    return handler


def _create_console_handler():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    return console_handler
