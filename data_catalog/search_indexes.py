"""Search indexes for the catalog using Django Haystack."""

from haystack.indexes import RealTimeSearchIndex, CharField
from haystack import site
from data_catalog.models import App, Data, Project


class AppIndex(RealTimeSearchIndex):
    """A search index for the Project model."""
    text = CharField(document=True, use_template=True)


class ProjectIndex(RealTimeSearchIndex):
    """A search index for the Project model."""
    text = CharField(document=True, use_template=True)


site.register(App, AppIndex)
site.register(Project, ProjectIndex)
