from bottle import hook, request, response


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
