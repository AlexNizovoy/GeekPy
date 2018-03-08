from django.contrib import admin
from stories.models import Askstories
from stories.models import Beststories
from stories.models import Newstories
from stories.models import Topstories
from stories.models import Jobstories
from stories.models import Showstories

# Register your models here.
admin.site.register(Askstories)
admin.site.register(Beststories)
admin.site.register(Newstories)
admin.site.register(Topstories)
admin.site.register(Jobstories)
admin.site.register(Showstories)
