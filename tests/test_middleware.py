from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase

from changuito.middleware import CartMiddleware
from changuito.proxy import CartProxy


class CartMiddlewareTestCase(TestCase):
    def setUp(self):
        self.cm = CartMiddleware()
        r = HttpRequest()
        r.session = {}
        r.user = AnonymousUser()
        self.request = r

    def test_process_request_without_cart(self):
        self.assertEqual(self.cm.process_request(self.request), None)
        self.assertIsInstance(self.request.cart, CartProxy)
