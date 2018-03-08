from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from api.serailizer import StorySerializer, StoryCategorySerializer, StoryTypeSerializer
from stories.models import StoryCategory, StoryType, Story

from api.tasks import parsing
import api.config as cfg
from hn_parser.config import CATEGORIES


def index(request):
    return render(request, 'api/index.html')


def get_category(request, category_name):
    # try get category from StoryTypes (like Ask, Story, Job)
    try:
        category = StoryType.objects.get(name=category_name)
        by_story_type = True
    except StoryType.DoesNotExist:
        try:
            # try get category from StoryCategories (like showstories, askstories etc.)
            category = StoryCategory.objects.get(name=category_name)
            by_story_type = False
        except StoryCategory.DoesNotExist:
            return HttpResponse(status=400)

    if by_story_type:
        serializer = StoryTypeSerializer(category)
    else:
        serializer = StoryCategorySerializer(category)
    return JsonResponse(serializer.data, safe=False)


def get_story(request, story_id):
    story = get_object_or_404(Story, story_id=story_id)
    serializer = StorySerializer(story)
    return JsonResponse(serializer.data, safe=False)


def get_story_from_type(request, story_type, story_id):
    # try get category from StoryTypes (like Ask, Story, Job)
    try:
        category = StoryType.objects.get(name=story_type)
    except StoryType.DoesNotExist:
        try:
            # try get category from StoryCategories (like showstories, askstories etc.)
            category = StoryCategory.objects.get(name=story_type)
        except StoryCategory.DoesNotExist:
            return HttpResponse(status=400)
    try:
        story = category.stories.get(story_id=story_id)
    except category.DoesNotExist:
        return HttpResponse(status=400)

    serializer = StorySerializer(story)
    return JsonResponse(serializer.data, safe=False)


def parser_categories(request):
    return JsonResponse({'categories': CATEGORIES}, safe=False)


def start_parsing(request, story_type):
    # try get admin username (or email if exist) as email
    users = User.objects.all()
    superusers = []
    email = []
    for user in users:
        if user.is_superuser:
            superusers.append(user)
    for user in superusers:
        try:
            validate_email(user.username)
            email.append(user.username)
        except ValidationError:
            try:
                validate_email(user.email)
                email.append(user.email)
            except ValidationError:
                pass
    if not email:
        email = request.GET.get('email')
        try:
            validate_email(email)
        except ValidationError:
            email = cfg.EMAIL_REPORT_FALLBACK

    parsing.delay(story_type, email)
    msg = {'message': f'Parsing started. After finish email will be send to {email}'}
    return JsonResponse(msg, safe=False)



