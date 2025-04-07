"""User URLs."""

# Django
from django.urls import path
from fpt.users.views import landing as users_views


app_name = "users"
urlpatterns = [
    path(route="", view=users_views.LandingView.as_view(), name="landing_page"),
]
