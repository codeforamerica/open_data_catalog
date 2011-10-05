"""Search indexes for the catalog using Django Haystack."""

import datetime
from haystack.indexes import *
from haystack import site
from data_catalog.models import App, Data, Project


class ProjectIndex(SearchIndex):
    """A search index for the Project model."""
    text = CharField(document=True, use_template=True)


site.register(Project, ProjectIndex)
