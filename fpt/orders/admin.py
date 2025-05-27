# Django
from django.contrib import admin

# Models
from fpt.orders.models import Order, Cart, CartItem


class CartItemInline(admin.StackedInline):
    """SubCategory inline admin."""

    model = CartItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order model admin."""

    list_display = ["user", "cart", "total", "status"]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "user__phone_number",
    ]
    list_filter = ["status"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Cart model admin."""

    list_display = ["user", "status", "session_key", "is_active"]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "user__phone_number",
    ]
    list_filter = ["status"]
    ordering = ["created"]
    inlines = [CartItemInline]
