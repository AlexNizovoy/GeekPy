from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('<category_name>', views.show_stories, name='show_stories'),
]
