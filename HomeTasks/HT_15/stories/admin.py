from django.contrib import admin

from stories.models import Story, StoryCategory, StoryType


admin.site.register(Story)
admin.site.register(StoryType)
admin.site.register(StoryCategory)