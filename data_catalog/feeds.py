"""Feeds for the data catalog."""

from django.contrib.syndication.views import Feed
from data_catalog.models import Project


class LatestProject(Feed):
    """A feed for the latest projects."""
    title = 'Projects'
    link = '/'
    description = 'New projects.'

    def items(self):
		return Project.objects.all().reverse()[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description
