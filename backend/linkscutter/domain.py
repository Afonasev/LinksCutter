"""
Domain specific layer
"""

import datetime as dt


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


class IRandomKeyProvider:

    def next(self) -> str:
        raise NotImplementedError


class LinkService:

    def __init__(
        self,
        repository: ILinkRepository,
        key_provider: IRandomKeyProvider,
    ):
        self._repository = repository
        self._key_provider = key_provider
        self._links_count = repository.count()

    def create(self, link: Link) -> Link:
        link.key = self._key_provider.next()
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
