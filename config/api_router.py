# Django

# Rest framework
from rest_framework.routers import DefaultRouter

# Viewsets
from fpt.orders.api.views.cart import CartItemViewSet, CartViewSet

router = DefaultRouter()
router.register(r"cart-items", CartItemViewSet, basename="cart-items")
router.register(r"cart", CartViewSet, basename="cart")


app_name = "api"
urlpatterns = router.urls
