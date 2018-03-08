from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

from cart.views import Cart
from order.models import OrderItem
from order.forms import CheckoutForm


@csrf_protect
def checkout(request):
    cart = Cart(request)
    context = dict()
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#the-save-method
            order = form.save()
            for product in cart.get_products():
                OrderItem.objects.create(order=order, product=product['product'], price=product['price'],
                                         quantity=product['quantity'])
            cart.clear()
            context['order_id'] = order.id
        else:
            messages.warning(request, 'Error while form validation!')
            return HttpResponseRedirect(reverse('cart:index'))
    else:
        form = CheckoutForm()
        context['form'] = form
    context['checkout_done'] = request.method == 'POST'
    return render(request, 'order/checkout.html', context=context)
