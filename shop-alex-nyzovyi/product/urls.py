"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from product.views import (index, subcategory_details, product_details)
from product.views import (api_index,
                           CurrencyList, CurrencyDetail, currency_dump, currency_default,
                           ProductDetail, CategoryList, SubcategoryList, VendorList)


app_name = 'product'
urlpatterns = [
    path('', index, name='index'),
    path('category/<int:pk>', subcategory_details, name='subcategory-details'),
    path('product/<int:pk>', product_details, name='product-details'),


    path('api/', api_index, name='api-index'),
    path('api/currency', CurrencyList.as_view(), name='api-currency'),
    path('api/currency/dump', currency_dump, name='api-currency-dump'),
    path('api/currency/default', currency_default, name='api-currency-default'),
    path('api/currency/<str:code>', CurrencyDetail.as_view(), name='api-currency-detail'),

    path('api/product/<int:pk>', ProductDetail.as_view(), name='api-product-detail'),

    path('api/categories', CategoryList.as_view(), name='api-categories'),
    path('api/subcategory/<int:pk>', SubcategoryList.as_view(), name='api-subcategory'),

    path('api/vendors', VendorList.as_view(), name='api-vendors'),
    path('api/vendors/<int:pk>', VendorList.as_view(), name='api-vendors-details'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
