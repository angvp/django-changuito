from decimal import Decimal

from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.test import TestCase

from changuito.models import Item
from changuito.proxy import CartProxy


class CartProxyTestCase(TestCase):
    def setUp(self):
        anon_user = AnonymousUser()
        r = HttpRequest()
        r.session = {}
        r.user = anon_user
        cart = CartProxy(r)
        self.anon_user = anon_user
        self.cart_model = cart.get_cart(r)
        self.cart_proxy = cart
        self.user = User.objects.create(username="user_for_sell",
                                        password="sold",
                                        email="example@example.com")
        self.request = r

    def _create_item_in_request(self):
        self.cart_proxy.add(product=self.user,
                            unit_price=Decimal("125"),
                            quantity=1)

    def _create_item_in_db(self, product=None, quantity=2, unit_price=125):
        product = self.user if product is None else product
        item = Item.objects.create(cart=self.cart_model,
                                   product=product,
                                   quantity=quantity,
                                   unit_price=unit_price)
        return item

    def test_cart_merge_user_anonuser(self):
        # anonymous user
        cart = self.cart_proxy
        # registered user
        user = self.user
        # lets create an item
        self._create_item_in_db(product=user, quantity=3, unit_price=100)
        # lets merge with the user that we created on the db
        cart = cart.replace(cart.cart.id, user)
        self.assertEquals(cart.id, 1)
        self.assertEquals(cart.user, user)

    def test_cart_clear(self):
        cart = self.cart_proxy
        user = self.user
        self._create_item_in_db(product=user)
        self.assertEquals(cart.is_empty(), False)
        cart.clear()
        self.assertEquals(cart.is_empty(), True)

    def test_cart_add_item(self):
        cart = self.cart_proxy
        self._create_item_in_request()  # this will create 1 item of 125
        self.assertEquals(cart.is_empty(), False)
        self.assertEquals(cart.cart.total_price(), 125)

    def test_cart_remove_item(self):
        cart = self.cart_proxy
        user = self.user
        item = self._create_item_in_db(product=user)
        cart.remove_item(item.id)
        self.assertEquals(cart.is_empty(), True)

    def test_proxy_get_item(self):
        cart = self.cart_proxy
        user = self.user
        item = self._create_item_in_db(product=user)
        item_copy = cart.get_item(item.id)
        self.assertEquals(item.id, item_copy.id)
        self.assertEquals(item.quantity, item_copy.quantity)

    def test_proxy_cart_checkout(self):
        cart = self.cart_proxy
        user = self.user
        self._create_item_in_db(product=user)
        cart.checkout()
        self.assertEquals(cart.cart.checked_out, True)

    def test_new_cart_after_checkout_anon_user(self):
        cart = self.cart_proxy
        cart.checkout()
        self.assertEquals(cart.cart.checked_out, True)
        cart2 = CartProxy(self.request)
        self.assertNotEquals(cart.cart, cart2.cart)
        self.assertEquals(cart2.cart.checked_out, False)

    def test_new_cart_after_checkout_user(self):
        r = HttpRequest()
        r.session = {}
        r.user = self.user

        cart = CartProxy(r)
        cart.checkout()
        self.assertEquals(cart.cart.checked_out, True)
        cart2 = CartProxy(r)
        self.assertNotEquals(cart.cart, cart2.cart)
        self.assertEquals(cart2.cart.checked_out, False)
