# Django
from django.db.models import Count

# Models
from fpt.products.models import Category


def category_context(request):
    subcategories_menu = {}
    url_kwargs = request.resolver_match.captured_kwargs
    categories = (
        Category.objects.prefetch_related("subcategory")
        .annotate(available_products_count=Count("category_product"))
        .all()
        .order_by("created")
    )
    category = categories.filter(slug_name=url_kwargs.get("category_slug")).first()
    if category:
        subcategories_menu = (
            category.subcategory.annotate(
                available_products_count=Count("subcategory_product")
            )
            .all()
            .order_by("created")
        )
    return {"categories_menu": categories, "subcategories_menu": subcategories_menu}
