"""URL patterns for the website."""

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('data_catalog.views',
    url(r'^$', 'home'),
    url(r'^data/$', 'data'),
    url(r'^apps/$', 'apps'),
    url(r'^ideas/$', 'ideas'),
    url(r'^submit/app/$', 'submit_app'),
    url(r'^submit/idea/$', 'submit_idea'),
    url(r'^submit/data/$', 'submit_data'),
    url(r'^(?P<name>\w+)\.txt$', 'send_text_file'),
)


urlpatterns += patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
