import time

from bottle import install, response


@install
def execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        body = func(*args, **kwargs)
        end = time.time()
        response.headers['X-Exec-Time'] = str(end - start)
        return body
    return wrapper
