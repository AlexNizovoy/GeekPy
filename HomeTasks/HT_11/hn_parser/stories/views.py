from django.core.cache import cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect


import json

from stories import config as cfg
from stories import models as s_models  # 's_models' used in eval() get_stories
from stories.forms import GetNewRecordsForm
from stories.helpers import parse_stories


# Create your views here.
@csrf_protect
def index(request):
    if request.method == 'POST':
        # Getting new records
        form = GetNewRecordsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            context = {'records': dict()}
            token = request.POST.get('csrfmiddlewaretoken')
            form_data_category = form.cleaned_data.get('category').lower()
            if form_data_category == 'all':
                # parse all categories
                for category_name in cfg.CATEGORIES:
                    # Parse new stories
                    data = parse_stories(category_name, token)
                    # Save new stories in DB
                    category = check_category(category_name)
                    if category:
                        write_records(category, data)

            elif form_data_category in cfg.CATEGORIES:
                # parse only one category
                data = parse_stories(form_data_category, token)
                # Save new stories in DB
                category = check_category(form.cleaned_data.get('category'))
                if category:
                    write_records(category, data)

            else:
                # if unknown category
                return HttpResponseRedirect('/')

            # for category_name in cfg.CATEGORIES:
            #     records = get_stories(category_name)
            #     context['records'][category_name] = records
            # context['categories'] = cfg.CATEGORIES
            # context['form'] = form
            # redirect to a new URL:
            return HttpResponseRedirect('/')
        else:
            # if bad form
            return HttpResponseRedirect('/')
    else:
        # Rendering existing records
        # Get all records
        # TODO
        form = GetNewRecordsForm()
        context = {'records': dict()}
        for category_name in cfg.CATEGORIES:
            records = get_stories(category_name)
            context['records'][category_name] = records
        context['categories'] = cfg.CATEGORIES
        context['form'] = form
        return render(request, 'stories/index.html', context)


def parsing_status(request):
    if request.method == 'GET':
        if request.GET.get('key'):
            if cache.get(request.GET.get('key')):
                value = cache.get(request.GET['key'])
                return HttpResponse(json.dumps({"msg": value}),
                                    content_type="application/json")
            else:
                return HttpResponse(json.dumps({'error': "No csrf value in \
cache", 'key': request.GET.get('key')}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'error': 'No parameter key in GET \
request'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error': 'No GET request'}),
                            content_type="application/json")


def get_stories(category_name):
    category = check_category(category_name)
    # Get records from category
    if category:
        records = category.objects.order_by('-rec_id')
    else:
        records = None

    return records


def check_category(category_name):
    # Check category_name for alpha's only for prevent injection
    if not category_name.isalpha():
        category = None
    else:
        try:
            category = eval('s_models.{}'.format(category_name.capitalize()))
        except Exception:
            category = None

    return category


def write_records(category, data):
    for record in data:
        # remove keys from record (unsupported by model)
        keys_to_del = []
        for key in record.keys():
            if key not in category.fields:
                keys_to_del.append(key)
        for key in keys_to_del:
            del record[key]

        # Check for existing record
        obj = category.objects.filter(rec_id=record["rec_id"])
        if obj:
            # Update
            obj.update(**record)
        else:
            # create
            category.objects.create(**record)
