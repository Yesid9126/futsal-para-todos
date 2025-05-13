# Django
from django.utils import timezone

# Models
from fpt.orders.models import Cart


def get_or_create_cart(request):
    session_key = request.session.session_key or request.session.create()

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True, status="OPEN")
        # Check cart anonymous exists and merge
        anonymous_cart = Cart.objects.filter(session_key=session_key, user__isnull=True, is_active=True, status="OPEN").first()
        if anonymous_cart and anonymous_cart != cart:
            for item in anonymous_cart.cart_item.all():
                existing = cart.cart_item.filter(product=item.product).first()
                if existing:
                    existing.quantity += item.quantity
                    existing.save()
                else:
                    item.cart = cart
                    item.save()
            anonymous_cart.is_active = False
            anonymous_cart.save()
        return cart
    else:
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None, is_active=True, status="OPEN")
        return cart
