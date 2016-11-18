"""
Application specific layer
"""

from . import settings
from .domain import ILinkRepository, Link, LinkService


class LinkRepository(ILinkRepository):

    """
    Basic inmemory ILinkRepository implementation
    """

    _links = {}

    def count(self) -> int:
        return len(self._links)

    def save(self, link: Link):
        self._links[link.key] = link
        return link

    def remove(self, link: Link):
        self._links.pop(link.key)

    def get(self, **kw) -> Link:
        return self._links[kw['key']]

    def find(self, page: int, size: int, **kw) -> Link:
        to_index = page * size
        from_index = to_index - size
        return list(self._links.values())[from_index:to_index]


def link_service_factory():
    return LinkService(repository=LinkRepository())


def serialize_link(link: Link) -> dict:
    return {
        'url': link.url,
        'key': link.key,
        'created_at': link.created_at.strftime(settings.DATETIME_FORMAT),
    }


def deserialize_link(link: dict) -> Link:
    return Link(**link)
