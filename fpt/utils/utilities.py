# Django
from django.utils import timezone

import random
from string import ascii_uppercase, digits, ascii_lowercase


def generate_reference_payment():
    """Generate reference  key for payment."""
    code_lenght = 10
    pool = ascii_uppercase + digits + ascii_lowercase
    reference = "{}{}{}".format(
        timezone.localdate().month,
        timezone.localdate().day,
        "".join(random.choices(pool, k=code_lenght)),
    )
    return reference


def update_products_stock(cart):
    cart_items = cart.cart_item.all()
    for cart_item in cart_items:
        product = cart_item.product
        quantity = cart_item.quantity
        product.stock = product.stock - quantity
        product.save()
    return "Update stock"