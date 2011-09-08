"""
Test cases for causes.
"""

from django.test import TestCase
from causes.models import Cause, Link, Supporter


class TestModels(TestCase):

    def test_that_a_cause_can_be_created(self):
        Cause.objects.create(name='Test', description='A test cause.',
                             video_url='http://vimeo.com/12345').save()
        self.assertQuerysetEqual(Cause.objects.all(), ['Test'],
                                 lambda cause: cause.name)

    def test_a_supporter_must_have_links_and_causes(self):
        cause = Cause.objects.create(name='Test', description='Test cause.',
                                     video_url='http://vimeo.com/12345')
        cause.save()
        link = Link.objects.create(url='http://test.com')
        link.save()
        supporter = Supporter.objects.create(name='Test')
        supporter.links.add(link)
        supporter.causes.add(cause)
        supporter.save()
        self.assertQuerysetEqual(Supporter.objects.all(), ['Test'],
                                 lambda supporter: supporter.name)
