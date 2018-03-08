from django.db import models
from .helpers import Record


class Askstories(Record):
    fields = Record.fields[:] + ['text', 'descendants', 'kids']

    text = models.TextField(null=True)
    descendants = models.IntegerField(null=True)
    kids = models.TextField(null=True)


class Beststories(Record):
    fields = Record.fields[:] + ['url', 'text', 'descendants', 'kids']
    # change URLField to TextField, because TextField == charfield(200)
    url = models.TextField(null=True)
    text = models.TextField(null=True)
    descendants = models.IntegerField(null=True)
    kids = models.TextField(null=True)


class Newstories(Record):
    fields = Record.fields[:] + ['url', 'text', 'descendants', 'kids']

    url = models.TextField(null=True)
    text = models.TextField(null=True)
    descendants = models.IntegerField(null=True)
    kids = models.TextField(null=True)


class Topstories(Record):
    fields = Record.fields[:] + ['url', 'text', 'descendants', 'kids']

    url = models.TextField(null=True)
    text = models.TextField(null=True)
    descendants = models.IntegerField(null=True)
    kids = models.TextField(null=True)


class Jobstories(Record):
    fields = Record.fields[:] + ['url']

    url = models.TextField(null=True)


class Showstories(Record):
    fields = Record.fields[:] + ['url', 'descendants', 'kids']

    url = models.TextField(null=True)
    descendants = models.IntegerField(null=True)
    kids = models.TextField(null=True)
