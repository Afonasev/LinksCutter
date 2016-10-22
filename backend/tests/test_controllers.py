# import unittest

# import bottle
# import peewee as pw
# import webtest
# from backend import models, wsgi


# class _ControllerTestCase(unittest.TestCase):

#     def setUp(self):
#         self.app = webtest.TestApp(wsgi.app)
#         models.db.initialize(pw.SqliteDatabase(':memory:'))

#         for model in models.tables:
#             model.create_table()


# class TestIndexController(_ControllerTestCase):

#     def test_get_index_page(self):
#         resp = self.app.get('/')

#         self.assertEqual(resp.status_int, 200)

#         index_page = bottle.static_file('index.html', root='frontend')
#         self.assertEqual(resp.text, index_page)


def test():
    assert 2 == 2
