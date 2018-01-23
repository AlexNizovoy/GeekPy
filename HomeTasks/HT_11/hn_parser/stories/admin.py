from django.contrib import admin
from .models import Askstories
from .models import Beststories
from .models import Newstories
from .models import Topstories
from .models import Jobstories
from .models import Showstories

# Register your models here.
admin.site.register(Askstories)
admin.site.register(Beststories)
admin.site.register(Newstories)
admin.site.register(Topstories)
admin.site.register(Jobstories)
admin.site.register(Showstories)
