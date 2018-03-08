from django.urls import path

from stories.views import IndexView, CategoryView

app_name = 'stories'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<category>', CategoryView.as_view(),
        name='category-details'),
]
