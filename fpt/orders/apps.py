from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class OrdersConfig(AppConfig):
    
    name = 'fpt.orders'
    varbose_name = _("Orders")
