# Django
from django import forms
from django.forms import modelformset_factory

# Models
from fpt.orders.models.carts import CartItem


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ["id", "quantity", "subtotal"]

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        product = self.instance.product
        size = self.instance.size
        product_by_size = product.stock_by_size.filter(size=size).first()
        stock_by_size = product_by_size.stock if product_by_size else 0
        if product_by_size and (stock_by_size <= 0):
            raise forms.ValidationError("La cantidad debe ser al menos 1.")
        if quantity > stock_by_size:
            raise forms.ValidationError(f"Solo hay {product.stock} unidades disponibles.")
        return quantity


CartItemFormSet = modelformset_factory(
    CartItem,
    form=CartItemForm,
    extra=0,
    can_delete=False
)