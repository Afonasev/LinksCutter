import unittest

from linkscutter.utils import random_str


class RandomStrTestCase(unittest.TestCase):

    def test(self):
        assert len(random_str(5)) == 5
        assert random_str(5) != random_str(5)
