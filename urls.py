"""URL patterns for the website."""

from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^accounts/login/$', redirect_to, {'url': '/login/'}),
    url(r'^accounts/', include('registration.urls')),
)
