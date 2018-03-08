from stories.models import StoryCategory


def categories(request):
    return {'categories': StoryCategory.objects.all().order_by('name')}
