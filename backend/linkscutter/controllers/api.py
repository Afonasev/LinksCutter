from bottle import redirect, response, request, static_file

from .. import settings
from ..application import serialize_link, deserialize_link
from .wsgi import app
from . import schemas


@app.get(r'/<key:re:[\d\w]+>')
def redirect_to_url(key):
    url = app.link_service.get(key=key).url
    if not url.startswith('http'):
        url = 'http://' + url
    redirect(url)


@app.get('/api')
@app.get('/api/v1')
def help():
    return schemas.api_v1


@app.get('/api/v1/links')
def get_links():
    links_page = app.link_service.find(**request.params)
    links_page['objects'] = [serialize_link(i) for i in links_page['objects']]
    return links_page


@app.get('/api/v1/links/<key>')
def get_link(key):
    return serialize_link(
        app.link_service.get(key=key),
    )


@app.post('/api/v1/links')
def add_link():
    return serialize_link(app.link_service.create(
        deserialize_link(request.json),
    ))


@app.hook('before_request')
def strip_path():
    """
    Ignore trailing slashes in routes
    """
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


@app.hook('after_request')
def enable_cors():
    """
    cross-origin resource sharing
    """
    response.headers.update({
        'access-control-allow-origin': '*',
        'access-control-allow-methods': 'put, get, post, delete, options',
        'access-control-allow-headers': (
            'authorization, origin, accept, content-type, x-requested-with',
        ),
    })


if settings.DEBUG:
    # nginx in production
    @app.get('/')
    def index():
        return static_file('index.html', settings.STATIC_PATH)

    @app.get(r'/static/<path:path>')
    def static(path):
        return static_file(path, settings.STATIC_PATH)
