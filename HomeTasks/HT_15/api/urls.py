from django.urls import path

from api.views import index, get_category, get_story, get_story_from_type, start_parsing, parser_categories

app_name = 'api'
urlpatterns = [
    path('', index, name='index'),
    path('<int:story_id>/', get_story, name='get-story'),
    path('<category_name>/', get_category, name='get-category'),
    path('<story_type>/<int:story_id>/', get_story_from_type, name='get-story-from-type'),
    path('parse', parser_categories, name='parser-categories'),
    path('parse/<story_type>', start_parsing, name='start-parsing'),
]
