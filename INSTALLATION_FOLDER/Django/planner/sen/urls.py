from django.conf.urls.defaults import patterns, include, url
from testapp.models import *
from testapp.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sen.views.home', name='home'),
    url(r'^sen/','sen.usrper.views.loginpage'),
    url(r'^signup/','sen.usrper.views.spage'),
    url(r'^putindatabase/','sen.usrper.views.signuppage'),
    url(r'^groups/', 'sen.groups.views.show_grp'),
    url(r'^(?P<gid>\d+)/getmem/', 'sen.groups.views.get_members'),   # 	HORIBBLE OUTPUT
    url(r'^accept/(?P<gid>\d+)/$', 'sen.groups.views.join_group'),
    url(r'^groups/(?P<gid>\d+)/reject/', 'sen.groups.views.delreq'),
    url(r'^addgroup/', 'sen.groups.views.create_group'),
    url(r'^groups/(?P<gid>\d+)/$', 'sen.groups.views.show_group'),
    url(r'^planner/', 'sen.testapp.views.planner_view'),  
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^login/','sen.usrper.views.loginpage'),  #for login page
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^logincheck/', 'sen.usrper.views.check_login'), #for logincheck
    url(r'^logout/', 'sen.usrper.views.logout'), #for logout
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
