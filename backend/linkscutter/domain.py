"""
Domain specific layer
"""

import datetime as dt

from . import settings
from .utils import random_str


class Entity:
    pass


class Link(Entity):

    def __init__(
        self,
        pk: int=None,
        url: str=None,
        key: str=None,
        created_at: dt.datetime=None,
    ):
        self.pk = pk
        self.url = url
        self.key = key
        self.created_at = created_at


class IRepository:

    def count(self) -> int:
        raise NotImplementedError

    def save(self, entity: Entity) -> Entity:
        raise NotImplementedError

    def get(self, **kw) -> Entity:
        raise NotImplementedError

    def find(self, page: int, size: int, **kw) -> [Entity]:
        raise NotImplementedError


class LinkService:

    def __init__(self, repository: IRepository):
        self._repository = repository

    def create(self, link: Link) -> Link:
        link.key = random_str(settings.MIN_KEY_LENGHT)
        link.created_at = dt.datetime.utcnow()
        self._repository.save(link)
        return link

    def get(self, **kw) -> Link:
        return self._repository.get(**kw)

    def find(self, page=1, size=20, **kw):
        return {
            'count': self._repository.count(),
            'page': page,
            'size': size,
            'objects': self._repository.find(page, size, **kw),
        }
