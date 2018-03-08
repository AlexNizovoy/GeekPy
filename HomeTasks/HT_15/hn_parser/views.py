from django.core.cache import cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages

import json

import hn_parser.config as cfg
from hn_parser.forms import GetNewRecordsForm
from hn_parser.helpers import parse_stories, write_records


@csrf_protect
def index(request):
    if request.method == 'POST':
        form = GetNewRecordsForm(request.POST)
        if not form.is_valid():
            messages.warning(request, 'Form not valid!')
            response = {'error': 'Form not valid!'}
            return HttpResponse(json.dumps(response),
                                content_type='application/json')
        token = request.POST.get('csrfmiddlewaretoken')
        # for test
        # token = 'token'
        form_data_category = form.cleaned_data.get('category').lower()
        if form_data_category == 'all':
            # parse all categories
            for category_name in cfg.CATEGORIES:
                # Parse new stories
                data = parse_stories(category_name, token)
                # Save new stories in DB
                if data:
                    write_records(data, token)

        elif form_data_category in cfg.CATEGORIES:
            # parse only one category
            data = parse_stories(form_data_category, token)
            # Save new stories in DB
            if data:
                write_records(data, token)

        else:
            # if unknown category
            messages.warning(request, 'Unknown category!')
            response = {'error': 'Unknown category!'}
            return HttpResponseRedirect(json.dumps(response),
                                        content_type='application/json')
        response = {'complete': True}
        return HttpResponse(json.dumps(response),
                            content_type='application/json')
    else:
        return HttpResponseRedirect(reverse('stories:index'))


def status(request):
    if request.method == 'GET':
        response = {'success': True}
        token = request.GET.get('key')
        # for test:
        # token = 'token'
        if token:
            if cache.get(token):
                value = cache.get(token)
                response['msg'] = value
            else:
                response['success'] = False
                response['error'] = 'No csrf value in cache'
                response['key'] = token
        else:
            response['success'] = False
            response['error'] = 'No parameter key in GET request'
    else:
        response = {'error': 'No GET request'}
    return HttpResponse(json.dumps(response), content_type='application/json')
