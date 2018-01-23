from django.contrib import admin

# Register your models here.
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
   list_display = ['name','blurb','goal','pledged','state']
