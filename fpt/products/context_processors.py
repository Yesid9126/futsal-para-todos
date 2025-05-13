# Django
from django.db.models import Count, Prefetch

# Models
from fpt.products.models import Category, ProductImage
from fpt.orders.models import Cart


def category_context(request):
    if request.user.is_authenticated:
        cart = (
            Cart.objects.filter(user=request.user, is_active=True, status="OPEN")
            .prefetch_related(
                "cart_item",
                "cart_item__product",
                Prefetch(
                    "cart_item__product__images",
                    queryset=ProductImage.objects.filter(is_principal=True),
                    to_attr="principal_image",
                ),
            )
            .first()
        )
    else:
        session_key = request.session.session_key or request.session.create()
        cart = (
            Cart.objects.filter(
                session_key=session_key, user=None, is_active=True, status="OPEN"
            )
            .prefetch_related(
                "cart_item",
                "cart_item__product",
                Prefetch(
                    "cart_item__product__images",
                    queryset=ProductImage.objects.filter(is_principal=True),
                    to_attr="principal_image",
                ),
            )
            .first()
        )
    cart_items = cart.cart_item.all() if cart else None
    subtotal = sum(item.subtotal for item in cart_items) if cart_items else None
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
    user = request.user if not request.user.is_anonymous else None
    return {
        "categories_menu": categories,
        "subcategories_menu": subcategories_menu,
        "user": user,
        "cart": cart,
        "cart_items": cart_items,
        "subtotal": subtotal,
    }
