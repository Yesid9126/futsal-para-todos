import hashlib

# Django
from django.views.generic.edit import FormView
from django.conf import settings
from django.urls import reverse_lazy

# Forms
from fpt.orders.forms.checkout import CheckoutForm

# Models
from fpt.users.models import UserAddress, User
from fpt.orders.models import Order

# Utils
from fpt.utils.mixins import EnsureCartExistsMixin
from fpt.utils.utilities import generate_reference_payment


class CheckoutView(EnsureCartExistsMixin, FormView):
    """Checkout view"""

    form_class = CheckoutForm
    template_name = "shop/checkout.html"
    success_url = reverse_lazy("orders:checkout")

    def dispatch(self, request, *args, **kwargs):
        self.cart = getattr(self.request, "cart", None)
        self.user = self.request.user if self.request.user.is_authenticated else None

        self.order = None
        if self.cart and self.user:
            self.order = Order.objects.filter(
                user=self.user,
                cart=self.cart,
                status="PENDING",
            ).first()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = (
            self.request.user if self.request.user.is_authenticated else None
        )
        return kwargs

    def form_valid(self, form):
        if self.user:
            # Usuario autenticado, actualizar sus datos
            self.user.first_name = form.cleaned_data["first_name"]
            self.user.last_name = form.cleaned_data["last_name"]
            self.user.email = form.cleaned_data["email"]
            self.user.phone_number = form.cleaned_data["phone_number"]
            self.user.save()

        else:
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone_number"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            self.user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone_number": phone,
                    "username": email,
                    "is_client": form.cleaned_data["create_account"],
                },
            )
            if not created:
                self.user.first_name = first_name
                self.user.last_name = last_name
                self.user.phone_number = phone
                self.user.save()

        # User address
        address, _ = UserAddress.objects.get_or_create(user=self.user)
        for field in form.Meta.fields:
            setattr(address, field, form.cleaned_data[field])
        address.save()

        # Create order
        if not self.order:
            self.order, _ = Order.objects.get_or_create(
                user=self.user, cart=self.cart, address=address, total=self.cart.total()
            )
            # Update cart status
            self.cart.status = "CHECKED_OUT"
            self.cart.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Si ya se creó la orden en esta sesión
        if self.order:
            amount_in_cents = int(self.order.total * 100)
            if not self.order.wompi_transaction_id:
                reference = generate_reference_payment()
                self.order.wompi_transaction_id = reference
                self.order.save()
            else:
                reference = self.order.wompi_transaction_id
            signature_string = (
                f"{reference}{amount_in_cents}COP{settings.WOMPI_INTEGRITY_KEY}"
            )
            integrity_signature = hashlib.sha256(
                signature_string.encode("utf-8")
            ).hexdigest()
            phone_number = self.user.phone_number
            prefix, number = phone_number[:3], phone_number[3:]
            context.update(
                {
                    "order": self.order,
                    "wompi_public_key": settings.WOMPI_PUB_KEY,
                    "wompi_reference": reference,
                    "url_redirect": "https://6fe965baebbf.ngrok-free.app",
                    "wompi_amount": amount_in_cents,
                    "wompi_signature": integrity_signature,
                    "user_email": self.user.email,
                    "user_phone": number,
                    "user_full_name": self.user.get_full_name(),
                    "prefix": prefix,
                }
            )
        return context
