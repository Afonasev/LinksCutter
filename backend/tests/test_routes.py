from unittest import TestCase, mock

from webtest import AppError, TestApp

from linkscutter.controllers import schemas, services  # noqa
from linkscutter.domain import Link  # noqa
from wsgi import app  # noqa

link_service_get_method = services.link_service.get


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

    def test_normal_redirect(self):
        test_link = 'http://www.test.com'
        test_key = 'test_key'

        services.link_service.get = mock.MagicMock(
            return_value=Link(
                url=test_link,
                key=test_key,
            ),
        )

        response = self.app.get('/' + test_key)
        assert response.status_code == 302
        assert response.location == 'http://www.test.com'

    def test_link_not_exists(self):
        test_key = 'test_key'

        services.link_service.get = mock.MagicMock(
            side_effect=KeyError,
        )

        with self.assertRaisesRegex(AppError, r'404'):
            self.app.get('/' + test_key)
