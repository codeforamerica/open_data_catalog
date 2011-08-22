"""Models for the data catalog."""

from django.db import models


class Tag(models.Model):
    """A model for an unique tag."""
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class App(models.Model):
    """A model for an application."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='apps')

    def __unicode__(self):
        return self.name


class Idea(models.Model):
    """A model for an ideas."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='ideas')

    def __unicode__(self):
        return self.name
