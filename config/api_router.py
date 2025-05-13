# Django

# Rest framework
from rest_framework.routers import DefaultRouter

# Viewsets
from fpt.orders.api.views.cart import CartItemViewSet

router = DefaultRouter()
router.register(r"cart-items", CartItemViewSet, basename="cart-items")


app_name = "api"
urlpatterns = router.urls
