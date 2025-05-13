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
from fpt.users.models import UserPromotionCode


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
        return self.render_forms(
            user_form=UserForm(instance=request.user),
            address_form=UserAddressForm(
                instance=getattr(request.user, "user_address", None)
            ),
            promo_form=PromoCodeForm(),
        )

    def get_context_data(self, **kwargs):
        context = {
            "user_codes": UserPromotionCode.objects.filter(user=self.request.user)
        }
        return context

    def post(self, request, *args, **kwargs):
        form_type = request.POST.get("form_type")
        user = request.user

        user_form = UserForm(instance=user)
        address_form = UserAddressForm(instance=getattr(user, "user_address", None))
        promo_form = PromoCodeForm()

        if form_type == "user":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Perfil actualizado correctamente.")
                return redirect(reverse_lazy("users:profile"))
        elif form_type == "user_address":
            address_form = UserAddressForm(
                request.POST, instance=getattr(user, "user_address", None)
            )
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = user
                address.save()
                messages.success(request, "Dirección actualizada.")
                return redirect(reverse_lazy("users:profile"))
        elif form_type == "user_code":
            promo_form = PromoCodeForm(request.POST, user=user)
            if promo_form.is_valid():
                promo_form.save()
                messages.success(request, "Código aplicado correctamente.")
                return redirect(reverse_lazy("users:profile"))

        return self.render_forms(user_form, address_form, promo_form, form_type)

    def render_forms(
        self, user_form=None, address_form=None, promo_form=None, active_form=None
    ):
        context = {
            "user_form": user_form
            if active_form == "user"
            else UserForm(instance=self.request.user),
            "address_form": address_form
            if active_form == "user_address"
            else UserAddressForm(
                instance=getattr(self.request.user, "user_address", None)
            ),
            "promo_form": promo_form if active_form == "user_code" else PromoCodeForm(),
            "active_tab": active_form,  # <- Nuevo
        }
        context.update(self.get_context_data())
        return render(self.request, self.template_name, context)
