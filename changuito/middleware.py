from .proxy import CartProxy
from django.utils.deprecation import MiddlewareMixin


class CartMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.cart = CartProxy(request)
