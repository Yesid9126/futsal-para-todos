from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class ProductsConfig(AppConfig):
    name = "fpt.products"
    verbose_name = _("Products")
