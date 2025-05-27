"""Orers URLs."""

# Django
from django.urls import path

# Views
from fpt.orders.views.carts import CartUpdateView

app_name = "orders"

urlpatterns = [
    path("carrito/", CartUpdateView.as_view(), name="cart_update"),
]
