"""
Domain specific layer
"""

import datetime as dt

from . import settings
from .utils import random_str


class Link:

    def __init__(
        self,
        url: str=None,
        key: str=None,
        created_at: dt.datetime=None,
    ):
        self.url = url
        self.key = key
        self.created_at = created_at

    @property
    def full_url(self):
        url = self.url
        if not url.startswith('http'):
            url = 'http://' + url
        return url


class ILinkRepository:

    def count(self) -> int:
        raise NotImplementedError

    def save(self, link: Link):
        raise NotImplementedError

    def remove(self, link: Link):
        raise NotImplementedError

    def get(self, key: str) -> Link:
        raise NotImplementedError

    def find(self, page: int, size: int, **kw) -> Link:
        raise NotImplementedError


class LinkService:

    def __init__(self, repository: ILinkRepository):
        self._repository = repository
        self._links_count = repository.count()

    def create(self, link: Link) -> Link:
        link.key = random_str(settings.MIN_KEY_LENGHT)
        link.created_at = dt.datetime.utcnow()
        self._repository.save(link)
        self._links_count += 1
        return link

    def get(self, **kw) -> Link:
        return self._repository.get(**kw)

    def find(self, page: int=1, size: int=20, **kw):
        return {
            'count': self._links_count,
            'page': page,
            'size': size,
            'objects': self._repository.find(page, size, **kw),
        }
