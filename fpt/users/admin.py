from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from fpt.users.forms.users import UserChangeForm
from .models import User, UserAddress, CodePromotion, UserPromotionCode


class UserAddressInline(admin.StackedInline):
    """SubCategory inline admin."""

    model = UserAddress
    extra = 1


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "photo",
                    "birthdate",
                    "discount_used",
                    "is_client",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["first_name", "last_name", "is_client", "phone_number"]
    search_fields = ["email", "first_name", "last_name"]
    inlines = [
        UserAddressInline,
    ]


@admin.register(CodePromotion)
class CodePromotionAdmin(admin.ModelAdmin):
    """Code promotion admin"""

    list_display = ["name", "date_init", "date_end"]


@admin.register(UserPromotionCode)
class CodePromotionUserAdmin(admin.ModelAdmin):
    """Code promotion admin"""

    list_display = ["user", "promotion_code", "is_used"]
