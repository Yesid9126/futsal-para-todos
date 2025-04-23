# Django
from django.core import paginator as pag


class BaseFilterMixin:
    """Base view for filters and pagination."""

    paginate_by = 4

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