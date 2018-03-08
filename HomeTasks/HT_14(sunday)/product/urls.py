from django.conf.urls import url

from product.views import index, subcategory_product, product_details


app_name = 'product'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<id>\d+)/$', subcategory_product,
        name='subcategory-product'),
    url(r'^(?P<id>\d+)/details/$', product_details,
        name='product-details'),
]