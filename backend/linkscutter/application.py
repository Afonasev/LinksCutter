"""
Application specific layer
"""

import sqlite3

from . import settings
from . import domain


class Link(domain.Link):

    @property
    def full_url(self):
        url = self.url
        if not url.startswith('http'):
            url = 'http://' + url
        return url


def connection_factory():
    connection = sqlite3.connect(
        settings.DATABASE,
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        check_same_thread=False,
    )
    connection.row_factory = sqlite3.Row
    return connection


class LinkRepository(domain.IRepository):

    def __init__(self, connection):
        self._connection = connection

    def count(self) -> int:
        return self._execute('SELECT count(*) FROM links')[0][0]

    def save(self, link: Link) -> Link:
        if link.pk is None:
            link.pk = self._execute_insert(
                '''
                INSERT INTO links (url, key, created_at)
                VALUES (?, ?, ?)
                ''',
                (link.url, link.key, link.created_at),
            )
        else:
            self._execute(
                '''
                UPDATE links SET url = ?, key = ?, created_at = ? WHERE pk = ?
                ''',
                (link.url, link.key, link.created_at, link.pk),
            )
        return link

    def get(self, key, **kw) -> Link:
        rows = self._execute('SELECT * FROM links WHERE key = ?', (key, ))
        if not rows:
            raise KeyError(key)
        return Link(**rows[0])

    def find(self, page: int, size: int, **kw) -> [Link]:
        query = 'SELECT * FROM links ORDER BY pk LIMIT ? OFFSET ?'
        rows = self._execute(query, (size, size * (page - 1)))
        return [Link(**r) for r in rows]

    def _execute(self, query, params=tuple()):
        with self._connection:
            return self._connection.execute(query, params).fetchall()

    def _execute_insert(self, query, params=tuple()):
        with self._connection:
            return self._connection.execute(query, params).lastrowid


def link_service_factory():
    db_connection = connection_factory()
    repository = LinkRepository(db_connection)
    return domain.LinkService(repository)


def serialize_link(link: Link) -> dict:
    return {
        'url': link.url,
        'key': link.key,
        'created_at': link.created_at.strftime(settings.DATETIME_FORMAT),
    }


def deserialize_link(link: dict) -> Link:
    return Link(**link)


def with_service(service_factory):
    def decorator(func):
        def wrap(*args, **kw):
            return func(service_factory(), *args, **kw)
        return wrap
    return decorator


with_link_service = with_service(link_service_factory)
