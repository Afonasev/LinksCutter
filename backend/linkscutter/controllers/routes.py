from bottle import abort, get, post, redirect, request, static_file

from linkscutter import settings
from linkscutter.application import with_link_service
from linkscutter.application import deserialize_link, serialize_link
from . import schemas


@get(r'/<key:re:[\d\w]+>')
@with_link_service
def redirect_to_url(link_service, key):
    try:
        redirect(link_service.get(key=key).full_url)
    except KeyError:
        abort(404)


@get('/api')
@get('/api/v1')
def get_schema():
    return schemas.api_v1


@get('/api/v1/links')
@with_link_service
def get_links(link_service):
    params = dict(request.params)
    for param in ('page', 'size'):
        if param in params:
            params[param] = int(params[param])

    links_page = link_service.find(**params)
    links_page['objects'] = [serialize_link(i) for i in links_page['objects']]
    return links_page


@get('/api/v1/links/<key>')
@with_link_service
def get_link(link_service, key):
    return serialize_link(
        link_service.get(key=key),
    )


@post('/api/v1/links')
@with_link_service
def add_link(link_service):
    return serialize_link(link_service.create(
        deserialize_link(request.json),
    ))


# nginx in production
@get('/')
def index():
    return static_file('index.html', settings.STATIC_PATH)


@get(r'/static/<path:path>')
def static(path):
    return static_file(path, settings.STATIC_PATH)
