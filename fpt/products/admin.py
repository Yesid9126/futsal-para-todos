from django.contrib import admin

# Models
from fpt.products.models import Product
from fpt.products.models.categories import Brand, Category, SubCategory
from fpt.products.models.products import ProductImage, ProductStockBySize

# Register your models here.


class SubCategoryInline(admin.StackedInline):
    """SubCategory inline admin."""

    model = SubCategory
    extra = 1
    readonly_fields = ["slug_name"]


class ProductImageInline(admin.StackedInline):
    """SubCategory inline admin."""

    model = ProductImage
    extra = 1


class ProductStockBySizeInline(admin.StackedInline):
    """ProductStockBySize inline admin."""

    model = ProductStockBySize
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin."""

    list_display = ["name", "brand", "price", "stock", "is_available"]
    search_fields = ["name", "brand__name", "category__name"]
    list_filter = ["is_available", "brand", "category"]
    readonly_fields = ["slug_name"]
    inlines = [ProductImageInline, ProductStockBySizeInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Brand admin."""

    list_display = ["name", "description"]
    search_fields = ["name"]
    list_filter = ["created", "modified"]
    readonly_fields = ["slug_name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin."""

    list_display = ["name", "description"]
    search_fields = ["name"]
    list_filter = ["created", "modified"]
    readonly_fields = ["slug_name"]
    inlines = [SubCategoryInline]
