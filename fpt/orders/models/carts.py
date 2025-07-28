# Django
from django.db import models

# Models
from fpt.utils.models import FptBaseModel


class Cart(FptBaseModel):
    """Cart model."""

    STATUS_CHOICES = (
        ("OPEN", "Abierto"),
        ("EXPIRED", "Expirado"),
        ("CHECKED_OUT", "Convertido en orden"),
        ("FINISHED", "Finalizado"),
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="carts",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    session_key = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        """Meta option."""

        verbose_name = "Carrito de usuario"
        verbose_name_plural = "Carritos de usuarios"

    def __str__(self):
        identifier = self.user.email if self.user else self.session_key
        return f"Cart ({identifier})"

    def total(self):
        return sum(item.subtotal for item in self.cart_item.all())

    def item_count(self):
        return sum(item.quantity for item in self.cart_item.all())


class CartItem(FptBaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_item")
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="product_item"
    )
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10)
    subtotal = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def stock_by_size(self):
        product_by_size = self.product.stock_by_size.filter(size=self.size)
        return product_by_size.stock if product_by_size else 0
