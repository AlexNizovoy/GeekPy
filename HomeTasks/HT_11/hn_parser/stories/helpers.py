
from django.db import models


class Record(models.Model):
    """Base class for records in tables - contain a common fields for
    all categories"""
    class Meta:
        # Create abstract class for inherit other records
        abstract = True

    rec_id = models.IntegerField()
    rec_type = models.CharField(max_length=15)
    score = models.IntegerField()
    time = models.DateTimeField()
    by = models.CharField(max_length=50)
    title = models.TextField()


def parse_stories(category_name):
    pass
