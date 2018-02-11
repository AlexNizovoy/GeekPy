from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views import generic
from django.urls import reverse

from todo.models import Project, Task
from todo.forms import ProjectForm, TaskForm


class IndexView(generic.ListView):
    template_name = 'todo/index.html'
    context_object_name = 'projects'
    queryset = Project.objects.all().order_by('-date_start')


def project_add(request):
    if request.method == 'GET':
        context = {
            'form': ProjectForm
        }
        return render(request, 'todo/project_form.html', context=context)
    else:
        form = ProjectForm(request.POST)
        if not form.is_valid():
            err = form.errors.as_data()
            msg = err.get('date_deadline')
            if msg:
                msg = msg[0].message
            else:
                msg = 'Invalid form data!'
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse('todo:index'))
        project = Project.objects.create(**form.cleaned_data)
        if project:
            messages.info(request, 'Project added!')
            return HttpResponseRedirect(reverse('todo:project-details',
                                                args=(project.pk,)))
        else:
            messages.warning(request, 'Something going wrong while create!')
            return HttpResponseRedirect(reverse('todo:index'))


def project_details(request, pk):
    context = {
        'project': get_object_or_404(Project, pk=pk)
    }
    return render(request, 'todo/project_details.html', context=context)


def task_add(request, project_id):
    if request.method == 'GET':
        project = get_object_or_404(Project, pk=project_id)
        context = {
            'project': project,
            'form': TaskForm(initial={'project': project.pk})
        }
        return render(request, 'todo/task_form.html', context=context)
    else:
        form = TaskForm(request.POST)
        if not form.is_valid():
            msg = 'Invalid form data!'
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse('todo:index'))
        task = Task.objects.create(**form.cleaned_data)
        if task:
            messages.info(request, 'Task added!')
        else:
            messages.warning(request, 'Something going wrong while create!')
        return HttpResponseRedirect(reverse('todo:project-details',
                                            args=(project_id,)))


def change_state(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    state = task.change_state()
    referer = request.META.get("HTTP_REFERER",
                               reverse('todo:project-details',
                                       args=(task.project_id,)))
    print("referer = ", referer, '\nstate = ', state)
    return HttpResponseRedirect(referer)
