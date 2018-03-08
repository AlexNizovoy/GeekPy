from django.shortcuts import render, get_object_or_404

from product.models import Product, Subcategory
from cart.forms import CartProductAddForm


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
        'product': get_object_or_404(Product, id=id),
        'form': CartProductAddForm(initial=dict(next=request.path, product_id=id))
    }
    return render(request, 'product/product-details.html', context)
