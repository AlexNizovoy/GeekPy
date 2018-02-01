from django.urls import path

from stories import views

urlpatterns = [
    path('', views.index, name='index'),
    path('parsing_status/', views.parsing_status, name='parsing_status'),
]
