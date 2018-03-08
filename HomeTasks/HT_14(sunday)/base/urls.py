from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'', include('product.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^admin/', admin.site.urls),
]
