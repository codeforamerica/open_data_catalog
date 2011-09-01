"""Models for the catalog."""

from django.db import models
from autoslug import AutoSlugField


class Cause(models.Model):
	"""An individual cause."""
	name = models.CharField(max_length=150)
	slug = AutoSlugField(populate_from='name', unique=True)
	video_url = models.URLField('Video URL', verify_exists=False)
	image = models.ImageField()
	description = models.TextField()

	def __unicode__(self):
		return self.name

	def embed_video(self):
		"""Code generated to embed a video -- either from YouTube or Vimeo."""
		# Get self.video_url
		# Parse the relevant information if vimeo
		# Generate the relevant embed code
		pass


class Supporter(models.Model):
	"""An individual who supports a cause."""
	name = models.CharField(max_length=150)
	causes = models.ManyToMany(Cause, related_name='Cause')
	links = models.OneToMany('Link', related_name='links')

	def __unicode__(self):
		return self.name


class Link(models.Model):
	"""A link to apps or repositories related to a cause."""
	url = models.URLField('URL', verify_exists=False)

	def __unicode__(self):
		return self.url
