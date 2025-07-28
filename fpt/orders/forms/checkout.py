# Django
from django import forms

# Models
from fpt.users.models.users import UserAddress
from fpt.orders.models.countries import Department


class CheckoutForm(forms.ModelForm):
    """User address forom."""

    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=17, required=True)
    create_account = forms.BooleanField(
        required=False, label="¿Deseas crear una cuenta?"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["department"].queryset = Department.objects.select_related(
            "country"
        ).order_by("name")
        if user and user.is_authenticated:
            # Si ya hay usuario, rellenamos los datos del formulario
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email
            self.fields["phone_number"].initial = user.phone_number

            try:
                address = user.user_address
                for field in self.Meta.fields:
                    self.fields[field].initial = getattr(address, field)
            except UserAddress.DoesNotExist:
                pass

    class Meta:
        model = UserAddress
        fields = [
            "country",
            "department",
            "address",
            "neighborhood",
            "additional_information",
            "secondary_contact",
        ]
        widgets = {
            "country": forms.Select(attrs={"class": "form-control select2-field"}),
            "department": forms.Select(attrs={"class": "form-control select2-field"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "neighborhood": forms.TextInput(attrs={"class": "form-control"}),
            "additional_information": forms.TextInput(attrs={"class": "form-control"}),
            "secondary_contact": forms.TextInput(attrs={"class": "form-control"}),
        }
