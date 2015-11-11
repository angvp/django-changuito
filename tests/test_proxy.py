from decimal import Decimal

from changuito.models import Item
from changuito.proxy import CartProxy, ItemDoesNotExist
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
import pytest


@pytest.fixture
def anon_user():
    user = AnonymousUser()
    return user


@pytest.fixture
def reg_user():
    user = User.objects.create(username="user_for_sell",
                               password="sold",
                               email="example@example.com")
    return user


@pytest.fixture
def rqst():
    r = HttpRequest()
    r.session = {}
    return r


@pytest.fixture
def rq_anonuser(anon_user, rqst):
    rqst.user = anon_user
    cart = CartProxy(rqst)
    return cart


@pytest.mark.django_db
def _create_item_in_db(user, cart_model, product=None, quantity=2,
                       unit_price=125):
    product = user if product is None else product

    item = Item.objects.create(cart=cart_model,
                               product=product,
                               quantity=quantity,
                               unit_price=unit_price)
    return item


@pytest.mark.django_db
def _create_item_in_request(rq_anonuser, reg_user):
    cart_proxy = rq_anonuser
    item = cart_proxy.add(product=reg_user,
                          unit_price=Decimal("125"),
                          quantity=1)
    return item


@pytest.mark.django_db
def test_cart_merge_user_anonuser(rq_anonuser, reg_user, rqst):
    # anonymous user
    cart = rq_anonuser
    # registered user
    user = reg_user
    # cart_model
    cart_model = rq_anonuser.get_cart(rqst)
    # lets create an item
    _create_item_in_db(user=user, cart_model=cart_model, product=user,
                       quantity=3, unit_price=100)
    # lets merge with the user that we created on the db
    cart = cart.replace(cart.cart.id, user)
    assert cart.id == 1
    assert cart.user == user


@pytest.mark.django_db
def test_cart_clear(rq_anonuser, reg_user, rqst):
    cart = rq_anonuser
    user = reg_user
    cart_model = rq_anonuser.get_cart(rqst)
    _create_item_in_db(user=user, cart_model=cart_model, product=user)
    assert cart.is_empty() is False
    cart.clear()
    assert cart.is_empty() is True


@pytest.mark.django_db
def test_cart_add_item(rq_anonuser, reg_user):
    cart = rq_anonuser
    # this will create 1 item of 125
    _create_item_in_request(rq_anonuser, reg_user)
    assert cart.is_empty() is False
    assert cart.cart.total_price() == 125


@pytest.mark.django_db
def test_cart_remove_item(rq_anonuser, reg_user, rqst):
    cart = rq_anonuser
    user = reg_user
    cart_model = cart.get_cart(rqst)
    item = _create_item_in_db(user=user, cart_model=cart_model, product=user)
    cart.remove_item(item.id)
    assert cart.is_empty() is True


@pytest.mark.django_db
def test_proxy_get_item(rq_anonuser, reg_user, rqst):
    cart = rq_anonuser
    user = reg_user
    cart_model = cart.get_cart(rqst)
    item = _create_item_in_db(user=user, cart_model=cart_model, product=user)
    item_copy = cart.get_item(item.id)
    assert item.id == item_copy.id
    assert item.quantity == item_copy.quantity


@pytest.mark.django_db
def test_proxy_cart_checkout(rq_anonuser, reg_user, rqst):
    cart = rq_anonuser
    user = reg_user
    cart_model = cart.get_cart(rqst)
    _create_item_in_db(user=user, cart_model=cart_model, product=user)
    cart.checkout()
    assert cart.cart.checked_out is True


@pytest.mark.django_db
def test_new_cart_after_checkout_anon_user(rq_anonuser, rqst):
    cart = rq_anonuser
    cart.checkout()
    assert cart.cart.checked_out is True
    cart2 = CartProxy(rqst)
    assert cart.cart != cart2.cart
    assert cart2.cart.checked_out is False


@pytest.mark.django_db
def test_new_cart_after_checkout_user(rqst, reg_user):
    rqst.user = reg_user
    cart = CartProxy(rqst)
    cart.checkout()
    assert cart.cart.checked_out is True
    cart2 = CartProxy(rqst)
    assert cart.cart != cart2.cart
    assert cart2.cart.checked_out is False


@pytest.mark.django_db
def test_cart_remove_unexistent_item(rq_anonuser, rqst):
    cart = rq_anonuser
    with pytest.raises(ItemDoesNotExist):
        cart.remove_item(60)


@pytest.mark.django_db
def test_cart_update_item(rq_anonuser, reg_user, rqst):
    cart = rq_anonuser
    user = reg_user
    cart_model = cart.get_cart(rqst)
    item = _create_item_in_db(user=reg_user, cart_model=cart_model,
                              product=user)
    assert cart.is_empty() is False
    assert item.quantity == 2
    new_cart = cart.update(product=item, quantity=3)
    assert int(new_cart.item_set.all()[0].quantity) == 3
