from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from product.models import Product
from cart.forms import CartInlineForm, CartProductAddForm

from decimal import Decimal
import json


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = {}
        self.cart = cart

    def add(self, product_id, quantity=1, add_quantity=True):
        """
        Add product to cart

        :param product_id: ID of instance of Product to add in cart
        :param quantity: quantity of added products
        :param add_quantity: if True - quantity increment total quantity of product, else - replace them
        :return: None
        """
        p_id = str(product_id)
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return None
        if p_id not in self.cart:
            self.cart[p_id] = {'quantity': 0, 'price': str(product.price), 'currency': str(product.currency)}
        in_stock = product.quantity - product.reserved

        tmp = quantity if not add_quantity else self.cart[p_id]['quantity'] + quantity
        if tmp > in_stock:
            raise AssertionError(f'Not enough items in stock. Choose up to {tmp} units.')
        else:
            if add_quantity:
                # Increment reserved
                product.reserved += quantity
            else:
                product.reserved += quantity - self.cart[p_id]['quantity']
            self.cart[p_id]['quantity'] = tmp
            product.save()
            self.save()

    def remove(self, product_id):
        p_id = str(product_id)
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return None
        if p_id in self.cart:
            released = self.cart.pop(p_id)
            product.reserved -= released['quantity']
            product.save()
            self.save()

    def save(self):
        # update the session cart
        self.session['cart'] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def get_products(self):
        products = Product.objects.filter(id__in=self.cart.keys())
        result = self.cart.copy()
        for product in products:
            result[str(product.id)]['product'] = str(product)
            result[str(product.id)]['product_id'] = product.id
            price, currency = product.get_price()
            result[str(product.id)]['price'] = str(round(price, 2))
            result[str(product.id)]['currency'] = str(currency)
        for item in result.values():
            item['total_price'] = str(Decimal(item['price']) * item['quantity'])
        return result.values()

    def get_total_cost(self):
        result = 0
        for item in self.get_products():
            result += Decimal(item['total_price'])
        return result

    def clear(self):
        # remove cart from session
        # сначала self.get_products(), потом для каждого продукта - self.remove
        if self.session.get('cart'):
            for product in list(self.get_products()):
                self.remove(product['product_id'])
            del self.session['cart']
            self.session.modified = True


@csrf_protect
def index(request):
    if request.method == 'POST':
        cart = Cart(request)
        form = CartProductAddForm(request.POST)
        if form.is_valid():
            # get form's data
            data = form.cleaned_data
            p_id = data.get('product_id')
            try:
                product = Product.objects.get(id=p_id)
            except Product.DoesNotExist:
                msg = {'error': 'Product does not exist!'}
            else:
                try:
                    cart.add(product.id, add_quantity=True)
                except AssertionError as e:
                    msg = {'error': e.args[0]}
                else:
                    msg = {'success': 'Added to cart!'}
        else:
            msg = {'error': 'Invalid form data!'}

        status = 500 if msg.get('error') else 200
        return JsonResponse(msg, status=status)
    else:
        return render(request, 'cart/cart.html')


@csrf_protect
def cart_change(request):
    if request.method == 'POST':
        cart = Cart(request)
        form = CartInlineForm(request.POST)
        if form.is_valid():
            # get form's data
            data = form.cleaned_data

            p_id = data.get('product_id')
            quantity = data.get('quantity')
            delete = data.get('delete')

            product = get_object_or_404(Product, id=p_id)

            if delete:
                cart.remove(product.id)
                messages.info(request, 'Product removed!')
            else:
                cart.add(product.id, quantity, add_quantity=False)
                messages.info(request, 'Product updated!')
        else:
            messages.warning(request, 'Invalid form data!')

    return HttpResponseRedirect(reverse('cart:index'))


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'Cart cleared!')
    return HttpResponseRedirect(reverse('product:index'))
