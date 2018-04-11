from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.models import (Currency, Category, Subcategory, Product, Vendor)
from product.models import (CurrencySerializer, ProductSerializer, CategorySerializer, SubcategoryListSerializer,
                            VendorSerializer)

import tempfile


@csrf_protect
def index(request):
    if request.method == 'GET':
        products = Product.objects.filter(on_main=True)
        page = request.GET.get('page')
        paginator = Paginator(products, settings.RECORDS_PER_PAGE)
        products = paginator.get_page(page)
        context = {'products': products,
                   'products_per_page': settings.RECORDS_PER_PAGE
                   }
        return render(request, 'product/index.html', context=context)
    elif request.method == 'POST':
        code = request.POST.get('code')
        if code:
            cache.set('currency', code)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(reverse('product:index'))
    else:
        return HttpResponseRedirect(reverse('product:index'))


def subcategory_details(request, pk):
    # in future - get products_per_page from User
    subcategory = get_object_or_404(Subcategory, pk=pk)
    products_list = subcategory.products.filter(active=True).order_by('view_count', 'out_of_stock')
    paginator = Paginator(products_list, settings.RECORDS_PER_PAGE)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products': products,
               'products_per_page': settings.RECORDS_PER_PAGE,
               'subcategory_name': subcategory.title}
    return render(request, 'product/subcategory-detail.html', context)


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk, active=True)
    product.view_count += 1
    product.save()
    context = {'product': product}
    return render(request, 'product/product-details.html', context=context)


# ---------------------
# ------- API ---------
# ---------------------
def api_index(request):
    return render(request, 'product/api-index.html')


# ---------- Currency -------
class CurrencyList(APIView):
    def get(self, request, format=None):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrencyDetail(APIView):
    def get(self, request, code, format=None):
        try:
            currency = Currency.objects.get(code=str(code).upper())
        except Currency.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CurrencySerializer(currency)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, code, format=None):
        try:
            currency = Currency.objects.get(code=str(code).upper())
        except Currency.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CurrencySerializer(currency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, code, format=None):
        try:
            currency = Currency.objects.get(code=str(code).upper())
        except Currency.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        currency.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def currency_dump(request, format=None):
    if request.method == 'GET':
        email = request.GET.get('email')
        response = Currency.dump_xls(email)
        if isinstance(response, bool):
            return Response({'message': f'Currency dump send to {email}'})
        else:
            return response
    elif request.method == 'POST':
        filename = request.FILES.get('xls_file')
        if not filename:
            return Response({'error': 'It is no file in POST data'}, status=status.HTTP_400_BAD_REQUEST)
        tmp = tempfile.NamedTemporaryFile(suffix='.xls')
        for chunk in filename.chunks():
            tmp.write(chunk)
        tmp.seek(0)
        created, updated = Currency.update_xls(tmp.name)
        tmp.close()
        response = {'message': f'File processed: {created} created, {updated} updated.'}

        return Response(response)


@api_view(['GET', 'POST'])
def currency_default(request, format=None):
    response = dict()
    if request.method == 'GET':
        try:
            currency = Currency().default_currency
        except Exception as e:
            response['error'] = str(e.args)
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            serializer = CurrencySerializer(currency)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        code = request.data.get('code')
        if not code:
            return Response({'error': '''Missing value 'code' for set default currency in POST!'''},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            Currency().default_currency = str(code).upper()
            currency = Currency().default_currency
        except Currency.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CurrencySerializer(currency)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---------- Product -------
class ProductDetail(APIView):
    def get(self, request, pk, format=None):
        currency = request.GET.get('currency')
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if currency:
            # Change view of product for use new currency
            product.price, product.currency = product.get_price(currency)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- Category -------
class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubcategoryList(APIView):
    def get(self, request, pk, format=None):
        try:
            subcategory = Subcategory.objects.get(pk=pk)
        except Subcategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        context = {'request': request}
        serializer = SubcategoryListSerializer(subcategory, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---------- Vendor -------
class VendorList(APIView):
    def get(self, request, pk=None, format=None):
        context = {'request': request}
        if pk:
            try:
                vendor = Vendor.objects.get(pk=pk)
            except Vendor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = VendorSerializer(vendor, context=context)
        else:
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, context=context, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
