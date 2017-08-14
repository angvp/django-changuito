from .proxy import CartProxy
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class CartMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.cart = CartProxy(request)
