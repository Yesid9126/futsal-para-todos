# Django
from django.db import models

# Models
from fpt.users.models import FutsalModel
from fpt.products.models.categories import Category, Brand


# Products model
class Product(FutsalModel):
    """Product model."""

    name = models.CharField("Nombre del producto", max_length=255)
    slug_name = models.SlugField("Slug de la categoría", max_length=40, unique=True)
    description = models.TextField("Descripción del producto", blank=True, null=True)
    stock = models.PositiveIntegerField("Stock del producto", default=0)
    sku = models.CharField("Product SKU", max_length=50, blank=True, null=True)
    is_available = models.BooleanField("Producto disponible", default=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    rating = models.PositiveIntegerField("Calificación del producto", default=0)
    price = models.PositiveIntegerField("Precio")
    percentage_discount = models.PositiveIntegerField("Porcentaje de descuento", default=0)

    class Meta:
        """Meta option."""

        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created", "-modified"]

    def __str__(self) -> str:
        """Return product name."""
        return self.name
