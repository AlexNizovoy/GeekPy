from django.conf.urls import url

from stories.views import IndexView, CategoryView

app_name = 'stories'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category>\w+)$', CategoryView.as_view(),
        name='category-details'),
]
