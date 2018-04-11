from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

from product.models import Product
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
                product_item = Product.objects.get(id=product['product_id'])
                OrderItem.objects.create(order=order, product=product_item, price=product['price'],
                                         quantity=product['quantity'], currency=product['currency'])
                product_item.quantity -= product['quantity']
                product_item.save()
            order.send_mail(copy_to_manager=True, request=request)
            context['order_id'] = order.id
            cart.clear()
        else:
            messages.warning(request, 'Error while form validation!')
            return HttpResponseRedirect(reverse('cart:index'))
    else:
        form = CheckoutForm()
        context['form'] = form
    context['checkout_done'] = request.method == 'POST'
    return render(request, 'order/checkout.html', context=context)
