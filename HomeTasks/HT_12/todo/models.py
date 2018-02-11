from django.db import models
from django.utils import timezone


class Project(models.Model):
    title = models.TextField(default='')
    description = models.TextField(default='')
    date_start = models.DateTimeField(auto_now=True)
    date_deadline = models.DateField(verbose_name='Deadline date')
    date_finish = models.DateTimeField(blank=True, null=True)

    @property
    def is_done(self):
        result = True
        for i in self.task_set.all():
            result = result and i.is_done
            if not result:
                break
        if result and not self.date_finish:
            self.date_finish = timezone.now()
            self.save()
        elif not result:
            self.date_finish = None
            self.save()
        return result

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.TextField(default='')
    description = models.TextField(default='')
    date_add = models.DateTimeField(auto_now=True)
    date_check = models.DateTimeField(blank=True, null=True)

    project = models.ForeignKey(Project, on_delete=None)

    is_done = models.BooleanField(default=False)

    def change_state(self):
        if self.is_done:
            self.is_done = False
            self.date_check = None
        else:
            self.is_done = True
            self.date_check = timezone.now()
        self.save()
        return self.is_done

    def __str__(self):
        return self.title
