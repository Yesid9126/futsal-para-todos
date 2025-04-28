"""Products views"""

# Django
from django.db.models import Count, Prefetch, Avg, Case, When
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Views
from django.views.generic import ListView, DetailView

# Models
from fpt.products.models import Product, ProductImage, ProductStockBySize
from fpt.users.models import User

# Mixins
from fpt.utils.mixins import BaseFilterMixin

# Forms
from fpt.products.forms import ProductCommentForm


class ProductListView(BaseFilterMixin, ListView):
    model = Product
    template_name = "shop/products_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        subcategory_slug = self.kwargs.get("subcategory_slug")
        if subcategory_slug:
            products = Product.objects.filter(
                sub_category__slug_name=subcategory_slug
            ).prefetch_related(
                "brand",
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.filter(is_principal=True),
                    to_attr="principal_image",
                ),
            )
        elif category_slug:
            products = Product.objects.filter(
                category__slug_name=category_slug
            ).prefetch_related(
                "brand",
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.filter(is_principal=True),
                    to_attr="principal_image",
                ),
            )
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
        self.request.session["category_slug"] = category_slug
        self.request.session["subcategory_slug"] = sub_category_slug
        context["total_products"] = products.count()
        qs = self._get_pagination(self.request, products)
        context["products"] = qs
        context["brands"] = brand_info
        context["base_url"] = base_url
        context["category_slug"] = category_slug
        context["sub_category_slug"] = sub_category_slug
        return context


class ProductDetailView(FormMixin, BaseFilterMixin, DetailView):
    """Product detail view"""

    template_name = "shop/product_detail.html"
    form_class = ProductCommentForm
    queryset = Product.objects.prefetch_related(
        "images",
        "product_comment",
        Prefetch(
            "stock_by_size",
            queryset=ProductStockBySize.objects.filter(stock__gt=0).order_by("size"),
            to_attr="product_sizes",
        ),
    ).annotate(
        average_rating=Avg("product_comment__rating"),
        total_reviews=Count("product_comment"),
        rating_5=Count(Case(When(product_comment__rating__gte=4.5, then=1))),
        rating_4=Count(
            Case(
                When(
                    product_comment__rating__gte=3.5,
                    product_comment__rating__lt=4.5,
                    then=1,
                )
            )
        ),
        rating_3=Count(
            Case(
                When(
                    product_comment__rating__gte=2.5,
                    product_comment__rating__lt=3.5,
                    then=1,
                )
            )
        ),
        rating_2=Count(
            Case(
                When(
                    product_comment__rating__gte=1.5,
                    product_comment__rating__lt=2.5,
                    then=1,
                )
            )
        ),
        rating_1=Count(Case(When(product_comment__rating__lt=1.5, then=1))),
    )
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"
    context_object_name = "product"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.request.session.get("category_slug")
        subcategory_slug = self.request.session.get("subcategory_slug")
        product = self.object
        comments = product.product_comment.all()
        qs = self._get_pagination(self.request, comments)
        context["comments"] = qs
        context["category_slug"] = category_slug
        context["subcategory_slug"] = subcategory_slug
        context["category_label"] = (
            category_slug.replace("_", " ").title() if category_slug else None
        )
        context["subcategory_label"] = (
            subcategory_slug.replace("_", " ").title() if subcategory_slug else None
        )
        total_reviews = product.total_reviews or 0
        if total_reviews > 0:
            rating_percentages = {
                5: round((product.rating_5 / total_reviews) * 100, 2),
                4: round((product.rating_4 / total_reviews) * 100, 2),
                3: round((product.rating_3 / total_reviews) * 100, 2),
                2: round((product.rating_2 / total_reviews) * 100, 2),
                1: round((product.rating_1 / total_reviews) * 100, 2),
            }
        else:
            rating_percentages = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        context["average_rating"] = (
            float(product.average_rating) if product.average_rating else 0
        )
        context["total_reviews"] = total_reviews
        context["rating_distribution"] = {
            5: product.rating_5,
            4: product.rating_4,
            3: product.rating_3,
            2: product.rating_2,
            1: product.rating_1,
        }
        context["rating_percentages"] = rating_percentages
        return context

    def get_success_url(self):
        return reverse_lazy(
            "products:product_detail", kwargs={"slug_name": self.object.slug_name}
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)

            if request.user.is_authenticated:
                comment.user = request.user
            else:
                name = form.cleaned_data.get("name")
                email = form.cleaned_data.get("email")
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={"username": email.split("@")[0], "name": name},
                )
                comment.user = user

            comment.product = self.object
            comment.save()
            return HttpResponseRedirect(self.get_success_url())
        return self.form_invalid(form)
