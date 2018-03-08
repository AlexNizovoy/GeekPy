from django.db import models


class StoryType(models.Model):
    # like Ask, Story, Job
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Story types'

    def __str__(self):
        return self.name


class StoryCategory(models.Model):
    # like Showstories, Jobstories, Newstories etc.
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Story categories'

    def __str__(self):
        return self.name


class Story(models.Model):
    # universal fields
    keys = ['story_type', 'story_id', 'score', 'time', 'by', 'title', 'url', 'text', 'descendants', 'kids']
    story_type = models.ForeignKey(StoryType, related_name='stories', on_delete=models.CASCADE)
    story_category = models.ForeignKey(StoryCategory, related_name='stories', on_delete=models.CASCADE)

    story_id = models.CharField(max_length=20)
    score = models.CharField(max_length=10)
    time = models.CharField(max_length=20)
    by = models.CharField(max_length=50)
    title = models.TextField()

    # optional fields
    url = models.TextField(null=True, default='')
    text = models.TextField(null=True, default='')
    descendants = models.TextField(null=True, default='')
    kids = models.TextField(null=True, default='')

    class Meta:
        verbose_name_plural = 'Stories'

    def __str__(self):
        return "{} #{}".format(self.story_type, self.story_id)

    @property
    def values(self):
        return [str(self.__getattribute__(i)) for i in self.keys]
