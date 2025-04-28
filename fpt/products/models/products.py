from slugify import slugify

# Django
from django.db import models

# Models
from fpt.users.models import FutsalModel, User
from fpt.products.models.categories import Category, Brand, SubCategory


# Products model
class Product(FutsalModel):
    """Product model."""

    name = models.CharField("Nombre del producto", max_length=255)
    slug_name = models.SlugField(
        "Slugname de la categoría", max_length=40, blank=True, null=True
    )
    description = models.TextField("Descripción del producto", blank=True, null=True)
    stock = models.PositiveIntegerField("Stock del producto", default=0)
    sku = models.CharField("Product SKU", max_length=50, blank=True, null=True)
    is_available = models.BooleanField("Producto disponible", default=True)
    best_seller = models.BooleanField("Más vendidos", default=False)
    newcomers = models.BooleanField("Recién llegados", default=False)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="category_product",
        blank=True,
        null=True,
    )
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        related_name="subcategory_product",
        blank=True,
        null=True,
    )
    rating = models.PositiveIntegerField("Calificación del producto", default=0)
    likes = models.PositiveIntegerField("Likes del producto", default=0)
    price = models.PositiveIntegerField("Precio")
    percentage_discount = models.PositiveIntegerField(
        "Porcentaje de descuento", default=0
    )

    class Meta:
        """Meta option."""

        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-created", "-modified"]

    def __str__(self) -> str:
        """Return product name."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method."""
        self.slug_name = slugify(self.name, separator="_")
        return super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.percentage_discount:
            return int(self.price - (self.price * self.percentage_discount / 100))
        return self.price


class ProductImage(FutsalModel):
    """Product image model."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField("Imagen del producto", upload_to="products/images/")
    is_principal = models.BooleanField(
        default=False,
        help_text="selecciona esta casilla si es la imagen principal del producto",
    )

    class Meta:
        """Meta option."""

        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imagenes de producto"

    def __str__(self) -> str:
        """Return product name."""
        return self.product.name


class ProductStockBySize(FutsalModel):
    """Product stock by size model."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="stock_by_size"
    )
    size = models.CharField("Talla", max_length=10)
    stock = models.PositiveIntegerField("Stock")

    class Meta:
        """Meta option."""

        verbose_name = "Stock por talla"
        verbose_name_plural = "Stock por tallas"

    def __str__(self) -> str:
        """Return product name."""
        return self.product.name


class ProductComment(FutsalModel):
    """Product comment model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_comments",
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_comment"
    )
    comment = models.TextField("Comentario del producto")
    likes = models.PositiveIntegerField(default=0)
    rating = models.FloatField("Rating", default=0)

    class Meta:
        """Meta option."""

        verbose_name = "Comentario del producto"
        verbose_name_plural = "comentarios del producto"

    def __str__(self):
        return f"Comentario en {self.product.name}"
