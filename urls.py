"""URL patterns for the website."""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.views.generic.simple import direct_to_template

admin.autodiscover()


urlpatterns = patterns('data_catalog.views',
    url(r'^$', 'home'),
    url(r'^apps$', 'apps'),
    url(r'^community$', 'community'),
    url(r'^data$', 'data'),
    url(r'^request/data$', 'request_data'),
    url(r'^projects$', 'projects'),
    url(r'^support/$', 'support'),
    url(r'^support/(?P<project_slug>[-\w]+)/$', 'support_project'),
    url(r'^(?P<resource_type>app|data|project)/(?P<slug>[-\w]+)/$',
         'individual_resource'),
    url(r'^community/(?P<username>[-\w]+)/$', 'community_member'),
    url(r'^thanks/$', 'thanks'),
    url(r'^search$', 'search'),
    url(r'^autocomplete$', 'autocomplete'),
    url(r'^submit/(?P<resource>app|data|project)$', 'submit_resource'),
    url(r'^(?P<name>\w+)\.txt$', 'send_text_file'),
)


urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('registration.urls')),
    url(r'^accounts/', include('registration.urls')),
)


# For pivot/testing...
urlpatterns += patterns('',
    url(r'^testing', direct_to_template, {'template': 'testing.html'}),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
          'document_root': settings.MEDIA_ROOT}))
