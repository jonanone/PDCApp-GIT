from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from plandechicasapp.views import home
from plandechicasapp.views import xd_receiver
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'plandechicasapp.views.home', name='home'),
    # url(r'^pdcapp/', include('pdcapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^xd_receiver\.html$', xd_receiver),
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    url(r'^signup/', 'plandechicasapp.views.signup', name='signup'),
    url(r'^login/', 'plandechicasapp.views.login', name='login'),
    url(r'^logout/$', 'plandechicasapp.views.logout_view', name='logout'),
    url(r'^dashboard/$', 'plandechicasapp.views.dashboard'),
    url(r'', include('django.contrib.auth.urls')),
    # Users urls
    url(r'^profile/$', 'plandechicasapp.views.view_self_profile', name='view_profile'),
    url(r'^messages/$', 'plandechicasapp.views.view_messages', name='view_messages'),
    url(r'^profile/edit/$', 'plandechicasapp.views.edit_profile', name='edit_profile'),
    url(r'^user/(?P<paramuser>\w{0,50})/$', 'plandechicasapp.views.view_profile', name='view_user_profile'),
    # TODO change view
    url(r'^friends/$', 'plandechicasapp.views.view_friends', name='view_user_friends'),
    url(r'^friends/requests/$', 'plandechicasapp.views.view_friend_requests', name='view_friend_requests'),
    url(r'^friends/add/$', 'plandechicasapp.views.view_friend_addition', name='view_friend_addition'),
    url(r'^pinkmoments/generator/$', 'plandechicasapp.views.view_pinkmoments_generator', name='view_pinkmoments_generator'),
    url(r'^calendar/$', 'plandechicasapp.views.view_calendar', name='view_user_calendar'),
    url(r'^calendar/(?P<month>\w{0,50})/$', 'plandechicasapp.views.view_other_calendar', name='view_other_calendar'),
    url(r'^pots/$', 'plandechicasapp.views.view_pots', name='view_user_pots'),
    url(r'^pots/(?P<pot_id>\w{0,50})/$', 'plandechicasapp.views.view_pot_details', name='view_pot_details'),
    url(r'^pots/(?P<pot_id>\w{0,50})/what_for/$', 'plandechicasapp.views.view_what_for', name='view_what_for'),
    url(r'^pots/(?P<pot_id>\w{0,50})/who/$', 'plandechicasapp.views.view_who', name='view_who'),
    url(r'^pots/(?P<pot_id>\w{0,50})/who/more/$', 'plandechicasapp.views.view_who2', name='view_who2'),   
    url(r'^pots/(?P<pot_id>\w{0,50})/what/$', 'plandechicasapp.views.view_what', name='view_what'),
    url(r'^new_pot/what_for/$', 'plandechicasapp.views.view_what_for', name='view_new_pot'),
    url(r'^boutique/$', 'plandechicasapp.views.view_boutique', name='view_boutique'),
    url(r'^fichajes/$', 'plandechicasapp.views.view_fichajes', name='view_fichajes'),
)
