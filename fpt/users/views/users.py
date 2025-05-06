"""Users views."""

# Django
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import FormView, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages

# Forms
from fpt.users.forms.users import (
    SignUpForms,
    CustomAuthenticationForm,
    UserForm,
    UserAddressForm,
    PromoCodeForm,
)

# Models


class LoginView(auth_views.LoginView):
    """Login view."""

    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True
    form_class = CustomAuthenticationForm
    template_name = "users/login.html"


class LogoutView(auth_views.LogoutView):
    """logout view."""

    next_page = "/login"


class SignUpView(FormView):
    template_name = "users/register.html"
    form_class = SignUpForms

    success_url = reverse_lazy("products:landing_page")

    def form_valid(self, form):
        user = form.save()
        remember_me = self.request.POST.get("rememberme")
        # Force login
        login(self.request, user)
        if remember_me:
            self.request.session.set_expiry(1209600)  # 2 semanas
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, View):
    template_name = "users/profile.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        user_form = UserForm(instance=user)
        address_form = UserAddressForm(instance=getattr(user, "user_address", None))
        promo_form = PromoCodeForm()
        return self.render_forms(user_form, address_form, promo_form)

    def post(self, request, *args, **kwargs):
        user = request.user
        user_form = UserForm(request.POST, request.FILES, instance=user)
        address_form = UserAddressForm(
            request.POST, instance=getattr(user, "user_address", None)
        )
        promo_form = PromoCodeForm(request.POST)
        form_type = request.POST.get("form_type")
        if form_type == "user" and user_form.is_valid():
            user_form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect(reverse_lazy("users:profile"))

        elif "user_address" and address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            messages.success(request, "Dirección actualizada.")
            return redirect(reverse_lazy("users:profile"))

        elif "apply_code" in request.POST and promo_form.is_valid():
            # Aquí va la lógica para el código promocional
            messages.success(request, "Código aplicado correctamente.")
            return redirect(reverse_lazy("users:profile"))

        else:
            messages.error(request, "Revisa los errores en el formulario.")
            return self.render_forms(user_form, address_form, promo_form)

    def render_forms(self, user_form, address_form, promo_form):
        return render(
            self.request,
            self.template_name,
            {
                "user_form": user_form,
                "address_form": address_form,
                "promo_form": promo_form,
            },
        )
