"""Products views"""

# Django
from django.db.models import Count
from django.urls import reverse_lazy

# Views
from django.views.generic import ListView


# Models
from fpt.products.models import Product

# Mixins
from fpt.utils.mixins import BaseFilterMixin


class ProductListView(BaseFilterMixin, ListView):
    model = Product
    template_name = "shop/products_list.html"
    context_object_name = "products"

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        subcategory_slug = self.kwargs.get("subcategory_slug")
        if subcategory_slug:
            products = Product.objects.filter(
                sub_category__slug_name=subcategory_slug
            ).prefetch_related("brand", "images")
        elif category_slug:
            products = Product.objects.filter(
                category__slug_name=category_slug
            ).prefetch_related("brand", "images")
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get("category_slug")
        sub_category_slug = self.kwargs.get("subcategory_slug")
        products = self.object_list
        brand_name = self.request.GET.get("brand")
        brand_info = products.values("brand__name").annotate(
            total_products_by_brand=Count("id")
        )
        if "subcategory_slug" in self.kwargs:
            base_url = False
        elif "category_slug" in self.kwargs:
            base_url = reverse_lazy(
                "products:product_list_by_category",
                kwargs={"category_slug": self.kwargs["category_slug"]},
            )
        if brand_name:
            products = products.filter(brand__name=brand_name)
        context["total_products"] = products.count()
        qs = self._get_pagination(self.request, products)
        context["products"] = qs
        context["brands"] = brand_info
        context["base_url"] = base_url
        context["category_slug"] = category_slug
        context["sub_category_slug"] = sub_category_slug
        return context
