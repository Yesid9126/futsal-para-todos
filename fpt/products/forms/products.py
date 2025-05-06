# Django
from django import forms

# Models
from fpt.products.models import ProductComment


class ProductCommentForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = ProductComment
        fields = ["first_name", "last_name", "email", "comment", "rating"]
