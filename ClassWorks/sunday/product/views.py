from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from product.models import Product, Subcategory


def index(request):
    context = {
        'products': Product.objects.filter(on_the_main=True)
    }
    return render(request, 'product/index.html', context)


def subcategory_product(request, id):
    context = {
        'subcategory': get_object_or_404(Subcategory, id=id)
    }
    return render(request, 'product/subcategory-product.html', context)


def product_details(request, id):
    context = {
        'product': get_object_or_404(Product, id=id)
    }
    return render(request, 'product/product-details.html', context)


def add_product_to_session(request, p_id):
    request.session.modified = True
    if 'products' not in request.session:
        request.session['products'] = []
    if p_id not in request.session['products']:
        request.session['products'].append(p_id)
        messages.info(request, 'Added to cart!')
    else:
        messages.info(request, 'Already exists!')


def cart(request):
    if request.method == 'POST':
        next_page = request.POST.get('next', '/')
        p_id = request.POST.get('product_id')
        add_product_to_session(request, p_id)
        return HttpResponseRedirect(next_page)
    else:
        if request.session.get('products'):
            products = Product.objects.filter(
                id__in=request.session['products']
            )
            return render(request, 'product/cart.html',
                          {'products': products})
        else:
            return render(request, 'product/cart.html')
