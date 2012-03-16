from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'planner.views.home', name='home'),
    # url(r'^planner/', include('planner.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^create_plan/$', 'create_plan.views.index'),
    url(r'^event/(?P<event_type_id>\d+)/(?P<event_id>\d+)/$', 'event.views.event_detail'),
    url(r'^event/(?P<event_type_id>\d+)/$','event.views.event_type_detail'),
    url(r'^event/$', 'event.views.all_events'), 
    #url(r'^plan/create/$','event.views.enter_date'),
    url(r'^plan/create/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$','event.views.create_plan'),
    url(r'^admin/', include(admin.site.urls)),
)
