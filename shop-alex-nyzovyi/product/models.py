# from django.contrib.admin import models
from django.core.cache import cache
from django.db import models
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse

from datetime import datetime

from product.helpers import send_out_data, dump_item_to_xls, update_item_from_xls


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    title = models.CharField(max_length=20)
    ratio = models.DecimalField(max_digits=7, decimal_places=4)
    default = models.BooleanField(blank=True, default=False)

    class Meta:
        ordering = ['code']
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.code

    def __init__(self, *args, **kwargs):
        super(Currency, self).__init__(*args, **kwargs)
        self.code = self.code.upper()

    @property
    def default_currency(self):
        try:
            return self.__class__.objects.get(default=True)
        except self.DoesNotExist:
            raise self.DoesNotExist('Please set default currency!')
        except self.MultipleObjectsReturned:
            raise self.MultipleObjectsReturned('Please set only ONE default currency!')
        
    @default_currency.setter
    def default_currency(self, code):
        try:
            currency = self.__class__.objects.get(code=code.upper())
        except self.DoesNotExist:
            raise self.DoesNotExist(f'Currency <{code}> does not exist.')

        # Execute custom deleter
        del self.default_currency
        currency.default = True
        currency.save()

    @default_currency.deleter
    def default_currency(self):
        for item in self.__class__.objects.all():
            if item.default:
                item.default = False
                item.save()

    @classmethod
    def update_xls(cls, filename):
        created, updated = update_item_from_xls(cls, filename, key_field='code')
        return created, updated

    @classmethod
    def dump_xls(cls, email=None):
        filename = 'currency_' + ''.join(str(datetime.now()).replace(' ', '_').split('.')[:-1]) + '.xls'
        data = dump_item_to_xls(cls)

        subject = f'Currencies dump from "{settings.PROJECT_NAME}"'
        msg = 'You request for currencies dump is Done. See attachment.'

        return send_out_data(data, filename, email, subject=subject, msg=msg)


class Category(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['title']

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    category = models.ManyToManyField(Category, related_name='subcategories')

    title = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Subcategories'
        ordering = ['title']

    def __str__(self):
        return self.title


class Vendor(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super(Vendor, self).__init__(*args, **kwargs)
        self.title = self.title.upper()


class ProductPropertiesKeys(models.Model):
    key = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class ProductPropertiesValues(models.Model):
    key = models.ForeignKey(ProductPropertiesKeys, on_delete=models.CASCADE)

    value = models.CharField(max_length=200)

    class Meta:
        ordering = ['key__key']

    def __str__(self):
        return f'{str(self.key)}: {self.value}'


class Product(models.Model):
    subcategory = models.ManyToManyField(Subcategory, related_name='products', blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.SET_NULL, blank=True, null=True)
    properties = models.ManyToManyField(ProductPropertiesValues)

    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(blank=True, default=0)
    reserved = models.PositiveIntegerField(blank=True, default=0, editable=False)
    out_of_stock = models.BooleanField(blank=True, default=False, editable=False)
    image = models.CharField(blank=True, default='', max_length=300)
    active = models.BooleanField(blank=True, default=False)
    on_main = models.BooleanField(blank=True, default=False)
    external = models.BooleanField(blank=True, default=False, editable=False)
    external_source = models.CharField(blank=True, default='', max_length=300)
    tags = models.TextField(blank=True, default='')
    view_count = models.PositiveIntegerField(blank=True, default=0, editable=False)
    created = models.DateTimeField(editable=False, null=True)
    modified = models.DateTimeField(editable=False, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # If exist link to external source (product from external shop API) - set .external to True
        if self.external_source:
            self.external = True
        # On save - update timestamps
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        # Check for Out-Of-Stock
        if self.quantity == 0 or self.quantity == self.reserved:
            self.out_of_stock = True
        # If Vendor is Null - disable product
        if not self.vendor:
            self.active = False
        return super(Product, self).save(*args, **kwargs)

    def get_price(self, use_currency=''):
        """
        Get price of product in default currency
        :param use_currency: Code of currency (like 'USD', 'eur' etc.). If exist - return price in selected currency, else return price in default currency
        :return: Tuple (price, currency_obj)
        """
        from_currency = self.currency
        try:
            if use_currency:
                to_currency = Currency.objects.get(code=str(use_currency).upper())
            else:
                to_currency = Currency.objects.get(code=str(cache.get('currency')).upper())
        except Currency.DoesNotExist:
            to_currency = Currency().default_currency

        return self.price * to_currency.ratio / from_currency.ratio, to_currency

    @classmethod
    def update_xls(cls, filename):
        created, updated = update_item_from_xls(cls, filename, key_field='title')
        return created, updated

    @classmethod
    def dump_xls(cls, email=None, sub_name=None):
        sub_name = sub_name or ''
        dt = ''.join(str(datetime.now()).replace(' ', '_').split('.')[:-1])
        filename = f'products_{sub_name + "_" if sub_name else ""}{dt}.xls'
        if sub_name:
            query = {'subcategory__title': sub_name}
        else:
            query = None
        data = dump_item_to_xls(cls, query=query)

        subject = f'Products dump from "{settings.PROJECT_NAME}"'
        msg = 'You request for products dump is Done. See attachment.'

        return send_out_data(data, filename, email, subject=subject, msg=msg)


# API
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.StringRelatedField(many=True)
    properties = serializers.StringRelatedField(many=True)
    currency = serializers.StringRelatedField(many=False)
    vendor = serializers.StringRelatedField(many=False)

    class Meta:
        model = Product
        fields = '__all__'


class SubcategoryRelatedSerializer(serializers.ModelSerializer):
    """
    Class for display Subcategories in list of all Categories
    """
    class Meta:
        model = Subcategory
        fields = ('id', 'title')


class SubcategoryListSerializer(serializers.ModelSerializer):
    """
    Class for display all products in selected Subcategory
    """
    products = serializers.HyperlinkedRelatedField(view_name='product:api-product-detail', many=True, read_only=True)

    class Meta:
        model = Subcategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategoryRelatedSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


# class ProductHyperlink(serializers.HyperlinkedRelatedField):
#     view_name = 'product:api-product-detail'
#
#     def get_products(self, vendor, view_name, request, format):
#         result = []
#         products = vendor.products.all()
#         subcategory = request.get('subcategory')
#         if subcategory:
#             for product in products:
#                 if product.subcategory.pk == subcategory:
#                     result.append(reverse(view_name, kwargs={'pk': product.pk}))
#         else:
#             for product in products:
#                 result.append(reverse('product:api-product-detail', kwargs={'pk': product.pk}))
#         return result


class VendorSerializer(serializers.ModelSerializer):
    products = serializers.HyperlinkedRelatedField(view_name='product:api-product-detail', many=True, read_only=True)
    # products = ProductHyperlink(read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'

