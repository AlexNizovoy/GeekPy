from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from product.models import Product
from cart.forms import CartProductAddForm, CartInlineForm


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = {}
        self.cart = cart

    def add(self, product, quantity=1, add_quantity=True):
        '''
        Add product to cart

        :param product: instance of Product to add in cart
        :param quantity: quantity of added products
        :param add_quantity: if True - quantity increment total quantity of product, else - replace them
        :return: None
        '''
        p_id = str(product.id)
        if p_id not in self.cart:
            self.cart[p_id] = {'quantity': 0, 'price': product.price}
        if add_quantity:
            self.cart[p_id]['quantity'] += quantity
        else:
            self.cart[p_id]['quantity'] = quantity
        self.save()

    def remove(self, product):
        p_id = str(product.id)
        if p_id in self.cart:
            del self.cart[p_id]
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
            result[str(product.id)]['product'] = product
        for item in result.values():
            item['total_price'] = item['price'] * item['quantity']
        return result.values()

    def get_total_cost(self):
        result = 0
        for item in self.get_products():
            result += item['total_price']
        return result

    def clear(self):
        # remove cart from session
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
            next_page = data.get('next', '/')
            p_id = data.get('product_id')
            quantity = data.get('quantity')

            product = get_object_or_404(Product, id=p_id)
            cart.add(product, quantity, add_quantity=True)
            messages.info(request, 'Added to cart!')

            return HttpResponseRedirect(next_page)
        else:
            messages.warning(request, 'Invalid form data!')
            return HttpResponseRedirect(request.path)
    else:
        form = CartInlineForm()
        return render(request, 'cart/cart.html', {'form': form})


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
                cart.remove(product)
                messages.info(request, 'Product removed!')
            else:
                cart.add(product, quantity, add_quantity=False)
                messages.info(request, 'Product updated!')
        else:
            messages.warning(request, 'Invalid form data!')

    return HttpResponseRedirect(reverse('cart:index'))


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'Cart cleared!')
    return HttpResponseRedirect(reverse('product:index'))