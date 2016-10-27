from bottle import abort, get, post, redirect, request, static_file

from . import schemas
from .services import link_service
from .. import settings
from ..application import deserialize_link, serialize_link


@get(r'/<key:re:[\d\w]+>')
def redirect_to_url(key):
    try:
        redirect(link_service.get(key=key).full_url)
    except KeyError:
        abort(404)


@get('/api')
@get('/api/v1')
def get_schema():
    return schemas.api_v1


@get('/api/v1/links')
def get_links():
    params = dict(request.params)
    for param in ('page', 'size'):
        if param in params:
            params[param] = int(params[param])

    links_page = link_service.find(**params)
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


if settings.DEBUG:
    # nginx in production
    @get('/')
    def index():
        return static_file('index.html', settings.STATIC_PATH)

    @get(r'/static/<path:path>')
    def static(path):
        return static_file(path, settings.STATIC_PATH)
