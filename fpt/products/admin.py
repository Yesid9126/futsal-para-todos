from django.contrib import admin

# Models
from fpt.products.models import Product

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin."""

    list_display = ["name", "brand", "price", "stock", "is_available"]
    search_fields = ["name", "brand__name", "category__name"]
    list_filter = ["is_available", "brand", "category"]
