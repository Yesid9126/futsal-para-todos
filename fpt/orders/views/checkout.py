# Django
from django.views.generic.edit import FormView

# Forms
from fpt.orders.forms.checkout import CheckoutForm

# Models
from fpt.users.models import UserAddress, User


class CheckoutView(FormView):
    """Checkout view"""
    form_class = CheckoutForm
    template_name = "shop/checkout.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user if self.request.user.is_authenticated else None
        return kwargs

    def form_valid(self, form):
        user = self.request.user if self.request.user.is_authenticated else None

        if user and user.is_authenticated:
            # Usuario autenticado, actualizar sus datos
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.phone_number = form.cleaned_data["phone_number"]
            user.save()

        else:
            # Usuario anónimo, crear uno nuevo
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone_number"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            # Buscar si ya existe usuario con ese email o teléfono
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone_number": phone,
                    "username": email,
                    "is_client": form.cleaned_data["create_account"],
                }
            )
            if not created:
                # Si ya existe, igual actualizamos su info
                user.first_name = first_name
                user.last_name = last_name
                user.phone_number = phone
                user.save()

        # Guardar dirección
        address, _ = UserAddress.objects.get_or_create(user=user)
        for field in form.Meta.fields:
            setattr(address, field, form.cleaned_data[field])
        address.save()
        return super().form_valid(form)

    def get_success_url(self):
        return "/checkout/thanks/"