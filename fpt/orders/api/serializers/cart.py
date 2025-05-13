# Rest framework
from rest_framework import serializers

# Models
from fpt.orders.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ["id", "product", "size", "quantity", "subtotal"]

