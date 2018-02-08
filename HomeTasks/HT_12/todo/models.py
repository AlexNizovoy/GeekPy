from django.db import models


class Project(models.Model):
    title = models.TextField(default='')
    description = models.TextField(default='')
    date_start = models.DateTimeField(auto_now=True)
    date_deadline = models.DateField()
    date_finish = models.DateTimeField()

    @property
    def is_done(self):
        result = True
        for i in self.task_set.all():
            result = result and i
            if not result:
                break
        return result


class Task(models.Model):
    title = models.TextField(default='')
    description = models.TextField(default='')
    date_add = models.DateTimeField(auto_now=True)
    date_check = models.DateTimeField()

    project = models.ForeignKey(Project, on_delete=None)

    is_done = False
