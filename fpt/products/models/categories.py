from slugify import slugify

# Django
from django.db import models

# Models
from fpt.users.models import FutsalModel


class SubCategory(FutsalModel):
    """SubCategory model."""

    name = models.CharField("Nombre de la subcategoría", max_length=255)
    slug_name = models.SlugField(
        "Slugname de la subcategoría", max_length=40, blank=True, null=True
    )
    description = models.TextField(
        "Descripción de la subcategoría", blank=True, null=True
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        related_name="subcategory",
        blank=True,
        null=True,
    )

    class Meta:
        """Meta option."""

        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"
        ordering = ["name"]

    def __str__(self) -> str:
        """Return subcategory name."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method."""
        self.slug_name = slugify(self.name, separator="_")
        return super().save(*args, **kwargs)


class Category(FutsalModel):
    """Category model."""

    name = models.CharField("Nombre de la categoría", max_length=255)
    slug_name = models.SlugField(
        "Slugname de la categoría", max_length=40, blank=True, null=True
    )
    description = models.TextField("Descripción de la categoría", blank=True, null=True)

    class Meta:
        """Meta option."""

        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self) -> str:
        """Return category name."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method."""
        self.slug_name = slugify(self.name, separator="_")
        return super().save(*args, **kwargs)


class Brand(FutsalModel):
    """Brand model."""

    name = models.CharField("Nombre de la marca", max_length=255)
    slug_name = models.SlugField(
        "Slugname de la marca", max_length=40, blank=True, null=True
    )
    description = models.TextField("Descripción de la marca", blank=True, null=True)

    class Meta:
        """Meta option."""

        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]

    def __str__(self) -> str:
        """Return brand name."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method."""
        self.slug_name = slugify(self.name, separator="_")
        return super().save(*args, **kwargs)
