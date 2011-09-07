"""Models for the data catalog."""

from django.db import models
from autoslug import AutoSlugField


class Tag(models.Model):
    """
    A model for unique tags. The name field is indexed in order for fast
    queries.
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __unicode__(self):
        return self.name


class Resource(models.Model):
    """An abstract model for resources submitted to the data catalog."""
    name = models.CharField(max_length=100, db_index=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField()

    class Meta:
        abstract = True


class App(Resource):
    """A model for a submitted application."""
    url = models.URLField('URL', verify_exists=False)
    tags = models.ManyToManyField(Tag, related_name='apps')

    def __unicode__(self):
        return self.name


class Data(Resource):
    """A model for submitted data."""
    url = models.URLField('URL', verify_exists=False, blank=True)
    tags = models.ManyToManyField(Tag, related_name='data')

    class Meta:
        verbose_name_plural = 'Data'

    def __unicode__(self):
        return self.name


class Idea(Resource):
    """A model for submitted ideas."""
    type = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='ideas')

    def __unicode__(self):
        return self.name
