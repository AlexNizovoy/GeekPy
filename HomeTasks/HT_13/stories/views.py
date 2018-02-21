from django.views import generic
from django.shortcuts import get_object_or_404

from stories.models import Category
from hn_parser.forms import GetNewRecordsForm


class IndexView(generic.ListView):
    template_name = 'stories/index.html'
    context_object_name = 'categories'
    queryset = Category.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GetNewRecordsForm()
        return context


class CategoryView(generic.ListView):
    template_name = 'stories/category.html'
    context_object_name = 'stories'

    def get_queryset(self):
        cat = get_object_or_404(Category, name=self.kwargs.get('category'))
        return cat.story_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GetNewRecordsForm()
        context['categories'] = Category.objects.all().order_by('name')
        return context
