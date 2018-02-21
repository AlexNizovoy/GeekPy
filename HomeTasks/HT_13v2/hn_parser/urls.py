from django.conf.urls import url

from hn_parser.views import index, status

app_name = 'hn_parser'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^status/', status, name='status'),
]
