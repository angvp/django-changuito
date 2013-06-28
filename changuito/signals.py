from django.contrib.auth.signals import user_logged_in


def merge_cart(sender, user, request, **kwargs):
    cart = request.cart
    # lets overwrite the previous cart in case the user had a car
    if not cart.is_empty():
        cart.replace(cart.cart.id, user)
        return True

    cart.__init__(request)


user_logged_in.connect(merge_cart)
