# Views
from django.views.generic import TemplateView
from django.db.models import Prefetch

# Models
from fpt.products.models import Product, ProductImage


class LandingView(TemplateView):
    """Landing view."""

    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(is_available=True).prefetch_related(
            Prefetch(
                "images",
                queryset=ProductImage.objects.filter(is_principal=True),
                to_attr="principal_image",
            )
        )
        context["best_sellers"] = products.filter(best_seller=True)[:8]
        context["newcomers"] = products.filter(newcomers=True)[:8]
        context["accessories"] = products.filter(category__name="Accesorios")
        return context


# Create your views here.
