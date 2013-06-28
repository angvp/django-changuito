from django.test import TestCase
from models import Cart, Item
from django.contrib.auth.models import User, AnonymousUser
import datetime
from decimal import Decimal
from django.http import HttpRequest

from proxy import CartProxy
from middleware import CartMiddleware


class CartItemsTestCase(TestCase):
    def setUp(self):
        self.cart = Cart.objects.create(creation_date=datetime.datetime.now(),
                checked_out=False)
        self.user = User.objects.create(username="user_for_sell",
                password="sold", email="example@example.com")

    def _create_item_in_db(self, product=None, quantity=2, unit_price=125):
        product = self.user if product is None else product
        item = Item.objects.create(cart=self.cart, product=product,
                quantity=quantity, unit_price=unit_price)
        return item

    def test_cart_creation(self):
        self.assertEquals(self.cart.id, 1)
        self.assertEquals(self.cart.is_empty(), True, "Cart must be empty")

    def test_item_creation(self):
        item = self._create_item_in_db()
        item_in_cart = self.cart.item_set.all()[0]
        self.assertEquals(item_in_cart, item,
                "First item in cart should be equal the item we created")
        self.assertEquals(self.cart.is_empty(), False)
        self.assertEquals(item_in_cart.product, self.user,
                "Product associated with the first item in cart should equal the user we're selling")
        self.assertEquals(item_in_cart.unit_price, Decimal("125"),
                "Unit price of the first item stored in the cart should equal 125")
        self.assertEquals(item_in_cart.quantity, 2,
                "The first item in cart should have 2 in it's quantity")

    def test_cart_total_price(self):
        item = self._create_item_in_db()
        item_two = self._create_item_in_db(unit_price=Decimal("100.00"),
                quantity=1)
        self.assertEquals(self.cart.total_price(), 350, "Price == (125*2)+100")

    def test_cart_item_price(self):
        item = self._create_item_in_db(quantity=4,
                unit_price=Decimal("3.20"))
        self.assertEquals(item.total_price, Decimal("12.80"))

    def test_item_unicode(self):
        item = self._create_item_in_db()
        self.assertEquals(item.__unicode__(), "%s units of User %s" % (2, self.user.id))

    def test_item_update_quantity(self):
        item = self._create_item_in_db()
        self.assertEquals(item.quantity, 2)
        item.update_quantity(7)
        self.assertEquals(item.quantity, 7)

    def test_item_update_contenttype(self):
        # Let's import different contenttype objects
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.sites.models import Site
        obj_site = Site.objects.all()[:1]
        obj_user = User()

        ctype_user = ContentType.objects.get_for_model(type(obj_user))
        ctype_site = ContentType.objects.get_for_model(type(obj_site[0]))

        item_user = self._create_item_in_db(quantity=1, unit_price=Decimal("100"))
        item_site = self._create_item_in_db(product=obj_site[0], quantity=2, unit_price=Decimal("100"))

        self.assertEquals(item_user.content_type, ctype_user)
        self.assertEquals(item_site.content_type, ctype_site)

        item_site.update_contenttype(obj_user)
        self.assertEquals(item_site.quantity, 3)
        self.assertEquals(item_site.total_price, 300)


class CartProxyTestCase(TestCase):
    def setUp(self):
        r = HttpRequest()
        r.session = {}
        r.user = anon_user
        cart = CartProxy(r)
        self.anon_user = AnonymousUser()
        self.cart = cart
        self.user = User.objects.create(username="user_for_sell",
                password="sold", email="example@example.com")
        self.request = r

    def _create_item_in_request(self):
        self.cart.add(product=self.user, unit_price=Decimal("125"), quantity=1)

    def _create_item_in_db(self, product=None, quantity=2, unit_price=125):
        product = self.user if product is None else product
        item = Item.objects.create(cart=self.cart, product=product,
                quantity=quantity, unit_price=unit_price)
        return item


class CartMiddlewareTestCase(TestCase):
    pass


"""

class CartProxyTestCase(TestCase):
    # Let's re-use some functions from the Model Test :)
    def _create_item_in_database(self, cart, product, quantity=1,
            unit_price=Decimal("100")):
        item = Item()
        item.cart = cart
        item.product = product
        item.quantity = quantity
        item.unit_price = unit_price
        item.save()

        return item

    def _create_item_in_request(self, cart_request):
        user = self._create_user_in_database()
        cart_request.add(product=user, unit_price=Decimal("125"), quantity=1)

    def _create_user_in_database(self):
        user = User(username="user_for_sell", password="sold",
                email="example@example.com")
        user.save()
        return user

    def test_cart_in_request(self):
        cart = self._create_cart_in_request()
        self.assertEquals(cart.cart.id, 1)

    def test_cart_user_is_anonymous(self):
        cart = self._create_cart_in_request()
        self.assertEquals(cart.cart.user, None)

    def test_cart_merge_user_anonuser(self):
        # anonymous user
        cart = self._create_cart_in_request()
        # registered user
        user = self._create_user_in_database()
        # lets create an item
        item = self._create_item_in_database(cart.cart, product=user, quantity=3, unit_price=100)
        # lets merge with the user that we created on the db
        cart = cart.replace(cart.cart.id, user)
        self.assertEquals(cart.id, 1)
        self.assertEquals(cart.user, user)

    def test_cart_clear(self):
        cart = self._create_cart_in_request()
        user = self._create_user_in_database()
        item = self._create_item_in_database(cart.cart, product=user, quantity=3, unit_price=100)
        self.assertEquals(cart.is_empty(), False)
        cart.clear()
        self.assertEquals(cart.is_empty(), True)

    def test_cart_add_item(self):
        cart = self._create_cart_in_request()
        self._create_item_in_request(cart) # this will create 1 item of 125
        self.assertEquals(cart.is_empty(), False)
        self.assertEquals(cart.cart.total_price(), 125)

    def test_cart_remove_item(self):
        cart = self._create_cart_in_request()
        user = self._create_user_in_database()
        item = self._create_item_in_database(cart.cart, product=user, quantity=3, unit_price=100)
        cart.remove_item(item.id)
        self.assertEquals(cart.is_empty(), True)

    def test_proxy_get_item(self):
        cart = self._create_cart_in_request()
        user = self._create_user_in_database()
        item = self._create_item_in_database(cart.cart, product=user, quantity=3, unit_price=100)
        item_copy = cart.get_item(item.id)
        self.assertEquals(item.id, item_copy.id)
        self.assertEquals(item.quantity, item_copy.quantity)
"""
