# Django
from django import forms

# Models
from fpt.products.models import ProductComment


class ProductCommentForm(forms.ModelForm):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = ProductComment
        fields = ["name", "email", "comment", "rating"]
