"""User URLs."""

# Django
from django.urls import path

# views
from fpt.users.views.users import SignUpView, LoginView, LogoutView, ProfileView

app_name = "users"
urlpatterns = [
    path(route="signup", view=SignUpView.as_view(), name="signup"),
    path(route="login/", view=LoginView.as_view(), name="login"),
    path(route="logout/", view=LogoutView.as_view(), name="logout"),
    path(route="profile/", view=ProfileView.as_view(), name="profile"),
]
