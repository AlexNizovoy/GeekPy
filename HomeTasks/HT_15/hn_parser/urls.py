from django.urls import path


from hn_parser.views import index, status

app_name = 'hn_parser'
urlpatterns = [
    path('', index, name='index'),
    path('status/', status, name='status'),
]
