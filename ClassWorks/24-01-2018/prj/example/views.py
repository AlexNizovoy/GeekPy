from django.shortcuts import render
from example.models import *


def index(request):
    context = {
        'categories': Book.objects.all()
    }
    return render(request, 'example/index.html', context)
