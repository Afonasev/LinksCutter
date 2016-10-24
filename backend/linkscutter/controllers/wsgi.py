from bottle import default_app

from .. import settings
from ..utils import init_logging

app = default_app()


def init():
    from . import hooks, middlewares, routes  # noqa pylint: disable=unused-variable

    app.config.SECRET_KEY = settings.SECRET_KEY
    init_logging()

    return app
