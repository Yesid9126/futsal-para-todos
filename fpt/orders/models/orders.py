# Django
from django.db import models

# Models


class Order(models.Model):
    """Order model."""

    STATUS_CHOICES = (
        ("PENDING", "Pendiente"),
        ("PAID", "Pagada"),
        ("FAILED", "Fallida"),
        ("CANCELLED", "Cancelada"),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    wompi_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    cart = models.OneToOneField(
        "orders.Cart", on_delete=models.CASCADE, related_name="orders"
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    address = models.ForeignKey(
        "users.UserAddress", on_delete=models.SET_NULL, null=True
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method_type = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    hook_data = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"

    def __str__(self):
        return f"Orden #{self.id} - {self.status}"
