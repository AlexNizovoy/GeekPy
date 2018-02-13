from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)


class Story(models.Model):
    # universal fields
    story_type = models.ForeignKey(Category, on_delete=models.CASCADE)

    story_id = models.CharField(max_length=20)
    score = models.CharField(max_length=10)
    time = models.CharField(max_length=20)
    by = models.CharField(max_length=50)
    title = models.TextField()

    # optional fields
    url = models.TextField(null=True)
    text = models.TextField(null=True)
    descendants = models.TextField(null=True)
    kids = models.TextField(null=True)
