#!/usr/bin/env python3
from bottle import default_app

from linkscutter import settings
from linkscutter.controllers import hooks, middlewares, routes  # noqa pylint: disable=unused-variable

app = default_app()
app.config.SECRET_KEY = settings.SECRET_KEY

if __name__ == '__main__':
    app.run(debug=True, reloader=True)
