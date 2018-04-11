from product.models import Category, Subcategory, Currency
from django.core.cache import cache


def categories(request):
    return {'categories': Category.objects.all().order_by('title')}


def currencies(request):
    return {'currencies': Currency.objects.all().order_by('code'),
            'session_currency': cache.get('currency') or str(Currency().default_currency)}
