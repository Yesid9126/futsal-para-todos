from rest_framework import serializers

# Models
from fpt.users.models import User
from fpt.orders.models import Order

# Utilities
from fpt.utils.utilities import update_products_stock


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


class TransactionSerializer(serializers.Serializer):
    """Transaction receptor serializer.

    Handle all transaction data.
    """

    event = serializers.CharField(max_length=100)
    data = serializers.JSONField()
    sent_at = serializers.DateTimeField()

    def create(self, data):
        """Storage membership based on transaction data."""
        possible_status = ["APPROVED", "VOIDED", "DECLINED", "ERROR"]
        transaction_data = data["data"]["transaction"]
        transaction_data["event"] = data["event"]
        status = transaction_data.get("status")
        if status in possible_status:
            if status == "APPROVED":
                reference = transaction_data.get("reference")
                order = Order.objects.filter(
                    wompi_transaction_id=reference, status="PENDING"
                ).last()
                if order:
                    transaction_id = transaction_data.get("id")
                    payment_method_type = transaction_data.get("payment_method_type")
                    order.status = "PAID"
                    order.hook_data = transaction_data
                    order.transaction_id = transaction_id
                    order.payment_method_type = payment_method_type
                    cart = order.cart
                    cart.status = "FINISHED"
                    order.save()
                    cart.save()
                    update_products_stock(cart)
        return status
