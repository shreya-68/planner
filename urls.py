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
    url(r'^create_plan/$', 'create_plan.views.index'),
    url(r'^events/(?<events_id>\d+)/$', 'event.views.detail'),
    
    
    url(r'^admin/', include(admin.site.urls)),
)
