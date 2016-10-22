from bottle import Bottle

from .. import settings
from ..utils import init_logging

app = Bottle()


def init():
    from . import api  # noqa pylint: disable=unused-import,unused-variable

    init_logging()
    app.config.SECRET_KEY = settings.SECRET_KEY

    return app
