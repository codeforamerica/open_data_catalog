"""Feeds for the latest causes."""

from django.contrib.syndication.views import Feed
from causes.models import Cause


class LatestCauses(Feed):
    """A feed for the latest causes."""
    title = 'Causes'
    link = '/'
    description = 'New causes.'

    def items(self):
		return Cause.objects.all().reverse()[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description
