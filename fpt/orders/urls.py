"""Orers URLs."""

# Django
from django.urls import path

# Views
from fpt.orders.views.carts import CartUpdateView
from fpt.orders.views.checkout import CheckoutView

app_name = "orders"

urlpatterns = [
    path("carrito/", CartUpdateView.as_view(), name="cart_update"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]
