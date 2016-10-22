from bottle import get, hook, post, redirect, request, response, static_file

from . import schemas
from .services import link_service
from .. import settings
from ..application import deserialize_link, serialize_link


@get(r'/<key:re:[\d\w]+>')
def redirect_to_url(key):
    redirect(link_service.get(key=key).full_url)


@get('/api')
@get('/api/v1')
def get_schema():
    return schemas.api_v1


@get('/api/v1/links')
def get_links():
    links_page = link_service.find(**dict(request.params))
    links_page['objects'] = [serialize_link(i) for i in links_page['objects']]
    return links_page


@get('/api/v1/links/<key>')
def get_link(key):
    return serialize_link(
        link_service.get(key=key),
    )


@post('/api/v1/links')
def add_link():
    return serialize_link(link_service.create(
        deserialize_link(request.json),
    ))


@hook('before_request')
def strip_path():
    """
    Ignore trailing slashes in routes
    """
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


@hook('after_request')
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
    @get('/')
    def index():
        return static_file('index.html', settings.STATIC_PATH)

    @get(r'/static/<path:path>')
    def static(path):
        return static_file(path, settings.STATIC_PATH)
