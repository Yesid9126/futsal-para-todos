# Views
from django.views.generic import TemplateView


class LandingView(TemplateView):
    """Landing view."""

    template_name = "users/landing_1.html"
