from unittest import TestCase

from webtest import AppError, TestApp

from linkscutter.application import link_service_factory  # noqa
from linkscutter.controllers import schemas  # noqa
from linkscutter.domain import Link  # noqa
from wsgi import app  # noqa


class APITestCase(TestCase):

    def setUp(self):
        self.app = TestApp(app)
        self.link_service = link_service_factory()

    def tearDown(self):
        self.link_service._repository._links.clear()


class RedirectToUrlTestCase(APITestCase):

    """
    GET /<key:str>
    """

    def test_normal_redirect(self):
        test_url = 'http://www.test.com'
        test_key = 'test_key'

        self.link_service._repository.save(Link(url=test_url, key=test_key))
        response = self.app.get('/' + test_key)

        assert response.status_code == 302
        assert response.location == test_url

    def test_link_not_exists(self):
        test_key = 'test_key'

        with self.assertRaisesRegex(AppError, r'404'):
            self.app.get('/' + test_key)


class GetSchemaTestCase(APITestCase):

    """
    GET /api
    GET /api/v1
    """

    def test_without_version(self):
        response = self.app.get('/api')
        assert response.json == schemas.api_v1

    def test_wit_version(self):
        response = self.app.get('/api/v1')
        assert response.json == schemas.api_v1


class GetLinksTestCase(APITestCase):

    """
    GET /api/v1/links
    """

    def test_empty(self):
        response = self.app.get('/api/v1/links')

        assert response.status_code == 200
        assert response.json['count'] == 0
        assert not response.json['objects']

    def test_get_without_conditions(self):
        test_links = [
            Link(url='test_url_1'),
            Link(url='test_url_2'),
        ]

        for link in test_links:
            self.link_service.create(link)

        response = self.app.get('/api/v1/links')

        assert response.status_code == 200
        assert response.json['count'] == 2

        for i in response.json['objects']:
            assert i['url'] in ('test_url_1', 'test_url_2')

    def test_size(self):
        test_links = [
            Link(url='test_url_1'),
            Link(url='test_url_2'),
        ]

        for link in test_links:
            self.link_service.create(link)

        response = self.app.get('/api/v1/links?size=1')

        assert response.status_code == 200
        assert response.json['count'] == 2
        assert response.json['size'] == 1
        assert len(response.json['objects']) == 1

    def test_page(self):
        test_links = [
            Link(url='test_url_1'),
            Link(url='test_url_2'),
        ]

        for link in test_links:
            self.link_service.create(link)

        response = self.app.get('/api/v1/links?page=2&size=1')

        assert response.status_code == 200
        assert response.json['count'] == 2
        assert response.json['size'] == 1
        assert response.json['page'] == 2
        assert len(response.json['objects']) == 1
        assert response.json['objects'][0]['url'] == 'test_url_2'


class GetLinkTestCase(APITestCase):

    """
    GET /api/v1/links/<key>
    """

    def test_exists_link(self):
        link = self.link_service.create(Link(url='test_url_1'))
        response = self.app.get('/api/v1/links/' + link.key)

        assert response.status_code == 200
        assert response.json['key'] == link.key
        assert response.json['url'] == link.url

    def test_not_exists_link(self):
        with self.assertRaisesRegex(AppError, r'404'):
            self.app.get(self.app.get('/api/v1/links/wrong_key'))


class AddLinkTestCase(APITestCase):

    """
    POST /api/v1/links
    """

    def test(self):
        link = {'url': 'test_url'}
        response = self.app.post_json('/api/v1/links', link)

        assert response.status_code == 200
        assert response.json['url'] == link['url']
        assert 'key' in response.json
        assert 'created_at' in response.json


class IndexTestCase(APITestCase):

    """
    get /
    """

    def test(self):
        response = self.app.get('/')
        assert response.status_code == 200


class StaticTestCase(APITestCase):

    """
    get /static/<path:path>
    """

    def test_exists_file(self):
        response = self.app.get('/static/index.html')
        assert response.status_code == 200

    def test_not_exists_file(self):
        with self.assertRaisesRegex(AppError, r'404'):
            self.app.get('/static/wrong.txt')
