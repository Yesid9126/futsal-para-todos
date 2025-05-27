# Rest framework
from rest_framework import serializers

# Models
from fpt.orders.models import CartItem, Cart


class CartModelSerializer(serializers.ModelSerializer):
    """Cart model serializer."""

    class Meta:
        model = Cart


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "product",
            "product_name",
            "product_image",
            "price",
            "size",
            "quantity",
            "subtotal",
        ]

    def get_product_image(self, obj):
        principal_image = obj.product.images.filter(is_principal=True).first()
        if principal_image:
            return principal_image.image.url
        return "https://placehold.co/600x700"

    def get_price(self, obj):
        if obj.product:
            return (
                obj.product.discounted_price
                if obj.product.discounted_price
                else obj.product.price
            )
        return 0
