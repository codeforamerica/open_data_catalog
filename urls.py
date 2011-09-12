"""URL patterns for the website."""

from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

admin.autodiscover()


urlpatterns = patterns('data_catalog.views',
    url(r'^$', 'home'),
    url(r'^apps$', 'apps'),
    url(r'^causes$', 'causes'),
    url(r'^data$', 'data'),
    url(r'^(?P<resource>app|data|cause)/(?P<slug>[-\w]+)$',
         'individual_resource'),
    url(r'^search$', 'search'),
    url(r'^autocomplete$', 'autocomplete'),
    url(r'^submit/(?P<resource>app|data|cause)/$', 'submit_resource'),
    url(r'^(?P<name>\w+)\.txt$', 'send_text_file'),
)


urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('registration.urls')),
)
