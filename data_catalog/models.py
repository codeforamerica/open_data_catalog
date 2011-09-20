"""Models for the data catalog."""

import re
from urllib import urlencode

from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from caching.base import CachingMixin, CachingManager


class Resource(models.Model):
    """An abstract model for resources submitted to the data catalog."""
    name = models.CharField(max_length=150, db_index=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField()
    tags = TaggableManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class App(Resource):
    """A model for a submitted application."""
    url = models.URLField('URL', verify_exists=False)
    image = models.ImageField(upload_to='apps', blank=True, null=True)


class Data(Resource):
    """A model for submitted data."""
    url = models.URLField('URL', verify_exists=False, blank=True)

    class Meta:
        verbose_name_plural = 'Data'


class Project(CachingMixin, Resource):
    """An individual project."""
    organization = models.CharField(max_length=150)
    video_url = models.URLField('Video URL', verify_exists=False)
    embed_url = models.URLField('Embed URL', verify_exists=False, blank=True)
    image = models.ImageField(upload_to='projects', blank=True, null=True)
    featured = models.BooleanField()
    objects = CachingManager()

    def save_embed_url(self):
        """Code generated to embed a video -- either from YouTube or Vimeo."""
        video_url = self.video_url
        hosting_provider, video_id = self.parse_video_id(video_url)
        if hosting_provider == 'youtube':
            embed_url = 'http://www.youtube.com/embed/%s' % (video_id)
        elif hosting_provider == 'vimeo':
            # Haven't added a color parameter yet.
            params = urlencode({
                'byline': 0,
                'portrait': 0,
                'title': 0,
            })
            embed_url = 'http://player.vimeo.com/video/%s?%s' % (video_id, params)
        else:
            # It was neither YouTube or Vimeo.
            raise Exception("You did not provide a correct YouTube or Vimeo link.")
        self.embed_url = embed_url

    def parse_video_id(self, video_url):
        """
        Given a video URL, parse the relevant hosting provider (YouTube,
        Vimeo) and unique video ID.
        """
        if 'youtube' in video_url:
            hosting_provider = 'youtube'
            video_id = re.search(r'v=(\w+)', video_url).group(1)
        elif 'vimeo' in video_url:
            hosting_provider = 'vimeo'
            video_id = re.search(r'\d+', video_url).group()
        else:
            hosting_provider, video_id = None, None
        return hosting_provider, video_id

    def only_one_featured(self):
        """Only one Project instance can be `featured` at a time."""
        if self.featured:
            for project in Project.objects.filter(featured=True):
                project.featured = False
                project.save()

    @staticmethod
    def featured_project():
        """Return the currently featured project or None."""
        try:
            featured = Project.objects.get(featured=True)
        except:
            featured = None
        return featured

    def save(self, **kwargs):
        """
        Overwrite the normal save method so that an `embed_url` is generated
        for the model.
        """
        self.save_embed_url()
        self.only_one_featured()
        super(Project, self).save(**kwargs)


class Supporter(models.Model):
    """An individual who supports a project."""
    user = models.OneToOneField(User)
    projects = models.ManyToManyField(Project, related_name='supporters')
    links = models.ManyToManyField('Link', related_name='supporters')

    def __unicode__(self):
        return self.user.username

    @staticmethod
    def add_project_supporter(project, user):
        """
        Get or create a supporter instance from a user, and add that
        supporter instance to a project.
        """
        if isinstance(project, unicode):
            # Then it's actually a project slug.
            project = Project.objects.get(slug=project)
        supporter, existed = Supporter.objects.get_or_create(user=user)
        project.supporters.add(supporter)

    @staticmethod
    def remove_project_supporter(project, user):
        """Remove a supporter from a project."""
        if isinstance(project, unicode):
            # Then it's actually a project slug.
            project = Project.objects.get(slug=project)
        supporter, existed = Supporter.objects.get_or_create(user=user)
        project.supporters.remove(supporter)


class Link(models.Model):
    """A link to apps or repositories related to a project."""
    url = models.URLField('URL', verify_exists=False)

    def __unicode__(self):
        return self.url
