"""Models for the data catalog."""

from django.db import models
from autoslug import AutoSlugField
from markdown import markdown


class Tag(models.Model):
    """A model for unique tags."""
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    def get_resources(self, name):
        """Return all resources linked to a tag."""
        instances = self.objects.filter(name__icontains=name)
        return instances


class Resource(models.Model):
    """An abstract model for resources submitted to the data catalog."""
    name = models.CharField(max_length=100)
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


class Idea(models.Model):
    """A model for submitted ideas."""
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    type = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='ideas')

    def __unicode__(self):
        return self.name
