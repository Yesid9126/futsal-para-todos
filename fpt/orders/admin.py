# Django
from django.contrib import admin
from django.utils.html import format_html

# Models
from fpt.orders.models import Order, Cart, CartItem, Country, Department


class CartItemInline(admin.StackedInline):
    """SubCategory inline admin."""

    model = CartItem
    extra = 1


class DepartmentInline(admin.StackedInline):
    """Department inline admin."""

    model = Department
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
    readonly_fields = ["formatted_address"]

    @admin.display(description="Dirección")
    def formatted_address(self, obj):
        if not obj.address:
            return "No hay dirección asociada"

        return format_html(
            """
            <table style="border-collapse: collapse;">
                <tr><th style="text-align: left; padding-right: 10px;">Contacto:</th><td>{}</td></tr>
                <tr><th style="text-align: left; padding-right: 10px;">Dirección:</th><td>{}</td></tr>
                <tr><th style="text-align: left; padding-right: 10px;">Barrio:</th><td>{}</td></tr>
                <tr><th style="text-align: left; padding-right: 10px;">Departamento:</th><td>{}</td></tr>
                <tr><th style="text-align: left; padding-right: 10px;">País:</th><td>{}</td></tr>
                <tr><th style="text-align: left; padding-right: 10px;">Tel. secundario:</th><td>{}</td></tr>
                <tr><th style="text-align: left; padding-right: 10px;">Información adicional:</th><td>{}</td></tr>
            </table>
            """,
            obj.address.user.phone_number or "-",
            obj.address.address or "-",
            obj.address.neighborhood or "-",
            obj.address.department or "-",
            obj.address.country or "-",
            obj.address.secondary_contact or "-",
            obj.address.additional_information or "-",
        )


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


@admin.register(Country)
class CouuntryAdmin(admin.ModelAdmin):
    """Order model admin."""

    list_display = ["name", "code"]
    inlines = [DepartmentInline]
