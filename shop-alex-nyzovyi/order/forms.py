from django.forms import ModelForm

from order.models import Order


class CheckoutForm(ModelForm):
    class Meta:
        model = Order
        exclude = ['created', 'updated', 'is_paid']
