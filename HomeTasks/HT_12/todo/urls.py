from django.conf.urls import url

from todo.views import (IndexView,
                        project_add,
                        project_details,
                        task_add,
                        change_state)

app_name = 'todo'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^add/$', project_add, name='project-add'),
    url(r'^(?P<pk>[0-9]+)/$', project_details, name='project-details'),
    url(r'^(?P<project_id>[0-9]+)/add/$', task_add, name='task-add'),
    url(r'^task/(?P<task_id>[0-9]+)/change-state/$', change_state,
        name='change-state'),
]
