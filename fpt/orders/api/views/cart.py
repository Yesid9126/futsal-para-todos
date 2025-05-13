# Django
from django.db import transaction

# Rest framework
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

# Models
from fpt.orders.api.serializers import CartItemSerializer
from fpt.orders.utils.carts import get_or_create_cart


class CartItemViewSet(
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet
        ):
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.cart = get_or_create_cart(request)

    def get_queryset(self):
        return self.cart.cart_item.select_related("product")

    def perform_create(self, serializer):
        with transaction.atomic():
            product = serializer.validated_data.get("product")
            quantity = serializer.validated_data.get("quantity", 1)
            price = product.discounted_price

            existing_item = self.cart.cart_item.select_for_update().filter(product=product).first()

            if existing_item:
                pass
            else:
                serializer.save(cart=self.cart, subtotal=price * quantity)

    def perform_update(self, serializer):
        serializer.save(cart=self.cart)
