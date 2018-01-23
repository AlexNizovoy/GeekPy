from django.db import models
from .helpers import Record


class Askstories(Record):
    text = models.TextField(null=True)
    descendants = models.IntegerField(null=True)
    kids = models.TextField(null=True)


class Beststories(Record):
    url = models.URLField(null=True)
    text = models.TextField(null=True)
    descendants = models.IntegerField(null=True)
    kids = models.TextField(null=True)


class Newstories(Record):
    url = models.URLField(null=True)
    text = models.TextField(null=True)
    descendants = models.IntegerField(null=True)
    kids = models.TextField(null=True)


class Topstories(Record):
    url = models.URLField(null=True)
    text = models.TextField(null=True)
    descendants = models.IntegerField(null=True)
    kids = models.TextField(null=True)


class Jobstories(Record):
    url = models.URLField(null=True)


class Showstories(Record):
    url = models.URLField(null=True)
    descendants = models.IntegerField(null=True)
    kids = models.TextField(null=True)
