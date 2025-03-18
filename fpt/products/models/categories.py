# Django
from django.db import models

# Models
from fpt.users.models import FutsalModel


class Category(FutsalModel):
    """Category model."""

    name = models.CharField("Nombre de la categoría", max_length=255)
    slug_name = models.SlugField("Slug de la categoría", max_length=40, unique=True)
    description = models.TextField("Descripción de la categoría", blank=True, null=True)

    class Meta:
        """Meta option."""

        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self) -> str:
        """Return category name."""
        return self.name


class Brand(FutsalModel):
    """Brand model."""

    name = models.CharField("Nombre de la marca", max_length=255)
    slug_name = models.SlugField("Slug de la marca", max_length=40, unique=True)
    description = models.TextField("Descripción de la marca", blank=True, null=True)

    class Meta:
        """Meta option."""

        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]

    def __str__(self) -> str:
        """Return brand name."""
        return self.name