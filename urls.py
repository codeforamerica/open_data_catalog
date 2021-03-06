"""URL patterns for the website."""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

admin.autodiscover()


urlpatterns = patterns('data_catalog.views',
    url(r'^$', 'home'),
    url(r'^about$', direct_to_template, {'template': 'about.html'}),
    url(r'^contact$', direct_to_template, {'template': 'contact.html'}),
    url(r'^faq$', direct_to_template, {'template': 'faq.html'}),
    url(r'^apps$', 'apps'),
    url(r'^community$', 'community'),
    url(r'^data$', 'data'),
    url(r'^request/data$', 'request_data'),
    url(r'^projects$', 'projects'),
    url(r'^support/$', 'support'),
    url(r'^support/(?P<project_slug>[-\w]+)/$', 'support_project'),
    url(r'^(?P<resource_type>app|project)/(?P<slug>[-\w]+)/$',
         'individual_resource'),
    url(r'^data/(?P<slug>[-\w]+)/$', 'redirect_to_data_couch'),
    url(r'^edit/(?P<resource_type>app|data|project)/$', 'edit_resource'),
    url(r'^edit/(?P<resource_type>app|data|project)/(?P<slug>[-\w]+)$',
         'edit_resource'),
    url(r'^my/projects$', 'my_projects'),
    url(r'^community/(?P<username>[-\w]+)/$', 'community_member'),
    url(r'^thanks/$', 'thanks'),
    url(r'^search$', include('haystack.urls')),
    url(r'^autocomplete$', 'autocomplete'),
    url(r'^submit/(?P<resource>app|data|project)$', 'submit_resource'),
    url(r'^(?P<name>\w+)\.txt$', 'send_text_file'),
)


urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('registration.urls')),
    url(r'^accounts/', include('registration.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
           {'document_root': settings.MEDIA_ROOT})
        )
