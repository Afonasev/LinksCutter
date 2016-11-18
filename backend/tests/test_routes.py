from unittest import TestCase

from webtest import AppError, TestApp

from linkscutter.application import link_service_factory  # noqa
from linkscutter.controllers import schemas  # noqa
from linkscutter.domain import Link  # noqa
from wsgi import app  # noqa


class APITestCase(TestCase):

    def setUp(self):
        self.app = TestApp(app)


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


class RedirectToUrlTestCase(APITestCase):

    """
    GET /<key:str>
    """

    def setUp(self):
        super().setUp()
        self.link_service = link_service_factory()

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
