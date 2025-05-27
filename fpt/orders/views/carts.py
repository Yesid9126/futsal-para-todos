# Django
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.forms import modelformset_factory

# Forms
from fpt.orders.forms.carts import CartItemForm

# Models
from fpt.orders.models.carts import CartItem


class CartUpdateView(FormView):
    template_name = "cart/cart_forms.html"
    form_class = CartItemForm
    success_url = reverse_lazy("products:landing_page")

    def get_formset(self, data=None):
        cart_items = getattr(self.request, "cart_items", CartItem.objects.none())
        CartItemFormSet = modelformset_factory(
            CartItem, form=CartItemForm, extra=0, can_delete=True
        )
        return CartItemFormSet(data=data, queryset=cart_items)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = kwargs.get("formset") or self.get_formset()
        return context

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response(self.get_context_data(formset=formset))

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Carrito actualizado correctamente.")
            return redirect(self.get_success_url())
        else:
            import ipdb

            ipdb.set_trace()
            messages.error(request, "Ocurrió u.")
            return self.render_to_response(self.get_context_data(formset=formset))
