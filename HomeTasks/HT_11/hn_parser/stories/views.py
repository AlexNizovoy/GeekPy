from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.http import HttpResponse

from . import config as cfg
from . import models as s_models  # 's_models' used in eval() get_stories
from .forms import GetNewRecordsForm
from .helpers import parse_stories


# Create your views here.
@csrf_protect
def index(request):
    if request.method == 'POST':
        # Getting new records
        form = GetNewRecordsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if form.cleaned_data.get('category') == 'all':
                # parse all categories
                context = {'records': []}
                for category_name in cfg.CATEGORIES:
                    parse_stories(category_name)
                    records = get_stories(category_name)
                    context['records'].append(records)
                context['categories'] = cfg.CATEGORIES
                context['form'] = form
            elif form.cleaned_data.get('category') in cfg.CATEGORIES:
                # parse only one category
                context = {'records': []}
                parse_stories(form.cleaned_data.get('category'))
                for category_name in cfg.CATEGORIES:
                    records = get_stories(category_name)
                    context['records'].append(records)
                context['categories'] = cfg.CATEGORIES
                context['form'] = form
            else:
                # if unknown category
                return HttpResponseRedirect('/')
            # redirect to a new URL:
            return render(request, 'stories/index.html', context)
        pass
    else:
        # Rendering existing records
        # Get all records
        # TODO
        form = GetNewRecordsForm()
        context = {'records': []}
        for category_name in cfg.CATEGORIES:
            records = get_stories(category_name)
            context['records'].append(records)
        context['categories'] = cfg.CATEGORIES
        context['form'] = form
        return render(request, 'stories/index.html', context)


def get_stories(category_name):
    # Check category_name for alpha's only for prevent injection
    if not category_name.isalpha():
        category = None
    else:
        try:
            category = eval('s_models.{}'.format(category_name.capitalize()))
        except Exception:
            category = None

    # Get records from category
    if category:
        records = category.objects.order_by('-rec_id')
    else:
        records = None

    return records
