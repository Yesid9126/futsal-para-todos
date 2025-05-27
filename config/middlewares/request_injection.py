# config/middlewares/request_injection.py

# Models
from fpt.products.models import ProductImage
from fpt.orders.models import Cart

# Django
from django.db.models import Prefetch, OuterRef, Subquery, IntegerField


class RequestInjectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_key = request.session.session_key or request.session.create()
        if request.user.is_authenticated:
            cart = (
                Cart.objects.filter(user=request.user, is_active=True, status="OPEN")
                .prefetch_related(
                    "cart_item",
                    "cart_item__product",
                    Prefetch(
                        "cart_item__product__images",
                        queryset=ProductImage.objects.filter(is_principal=True),
                        to_attr="principal_image",
                    ),
                )
                .first()
            )
        else:
            cart = (
                Cart.objects.filter(session_key=session_key, user=None, is_active=True, status="OPEN")
                .prefetch_related(
                    "cart_item",
                    "cart_item__product",
                    Prefetch(
                        "cart_item__product__images",
                        queryset=ProductImage.objects.filter(is_principal=True),
                        to_attr="principal_image",
                    ),
                )
                .first()
            )

        request.cart = cart
        request.cart_items = cart.cart_item.all() if cart else []

        return self.get_response(request)
