from .proxy import CartProxy


class CartMiddleware(object):

    def process_request(self, request):
        request.cart = CartProxy(request)
