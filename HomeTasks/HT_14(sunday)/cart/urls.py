from django.conf.urls import url

from cart.views import index, cart_change, cart_clear


app_name = 'cart'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^change/$', cart_change, name='change'),
    url(r'^clear/$', cart_clear, name='clear'),
]