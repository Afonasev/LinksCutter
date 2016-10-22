from bottle import Bottle

from .. import settings
from ..application import link_service_factory
from ..utils import init_logging


app = Bottle()


def init():
    from . import api  # noqa

    init_logging()
    app.config.SECRET_KEY = settings.SECRET_KEY
    app.link_service = link_service_factory()

    return app
