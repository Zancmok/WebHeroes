from unittest import TestCase


class WebAPITest(TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
