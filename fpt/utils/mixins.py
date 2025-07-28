# Django
from django.core import paginator as pag
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import AccessMixin


class BaseFilterMixin:
    """Base view for filters and pagination."""

    def get_paginate_by(self, queryset=None):
        """Override this method in views to set paginate_by dynamically."""
        return getattr(self, "paginate_by", 10)

    def _get_pagination(self, request, qs):
        page = request.GET.get("page", 1)
        paginator = pag.Paginator(qs, self.paginate_by)
        try:
            qs_paginated = paginator.page(page)
        except pag.PageNotAnInteger:
            qs_paginated = paginator.page(1)
        except pag.EmptyPage:
            qs_paginated = paginator.page(paginator.num_pages)
        return qs_paginated


class EnsureCartExistsMixin(AccessMixin):
    """
    Verifica si el request tiene un carrito válido.
    Si no lo tiene, redirecciona a la página principal.
    """

    def dispatch(self, request, *args, **kwargs):
        cart = getattr(request, "cart", None)

        if not cart or cart.status != "OPEN":
            return redirect(reverse("products:landing_page"))

        return super().dispatch(request, *args, **kwargs)
