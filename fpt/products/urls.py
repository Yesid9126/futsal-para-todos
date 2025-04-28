"""Shop URLs."""

# Django
from django.urls import path

# Views
from fpt.products.views.landing import LandingView
from fpt.products.views.products import ProductListView, ProductDetailView


app_name = "products"
urlpatterns = [
    path(route="", view=LandingView.as_view(), name="landing_page"),
    path(
        route="producto/<str:slug_name>/",
        view=ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        route="<slug:category_slug>/",
        view=ProductListView.as_view(),
        name="product_list_by_category",
    ),
    path(
        route="<slug:category_slug>/<slug:subcategory_slug>/",
        view=ProductListView.as_view(),
        name="product_list_by_subcategory",
    ),
]
