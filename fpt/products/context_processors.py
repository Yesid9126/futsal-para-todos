# Django
from django.db.models import Count

# Models
from fpt.products.models import Category


def category_context(request):
    cart = getattr(request, "cart", None)
    cart_items = getattr(request, "cart_items", [])

    subtotal = sum(item.subtotal for item in cart_items) if cart_items else None

    subcategories_menu = {}
    url_kwargs = (
        request.resolver_match.captured_kwargs if request.resolver_match else {}
    )

    categories = (
        Category.objects.prefetch_related("subcategory")
        .annotate(available_products_count=Count("category_product"))
        .order_by("created")
    )

    category = categories.filter(slug_name=url_kwargs.get("category_slug")).first()
    if category:
        subcategories_menu = category.subcategory.annotate(
            available_products_count=Count("subcategory_product")
        ).order_by("created")

    user = request.user if request.user.is_authenticated else None

    return {
        "categories_menu": categories,
        "subcategories_menu": subcategories_menu,
        "user": user,
        "cart": cart,
        "cart_items": cart_items,
        "subtotal": subtotal,
    }
