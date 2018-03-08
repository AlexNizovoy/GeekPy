from django.conf.urls import url

from order.views import checkout


app_name = 'order'
urlpatterns = [
    url(r'^checkout/$', checkout, name='checkout'),
]
