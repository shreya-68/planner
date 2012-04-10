from django.conf.urls.defaults import patterns, include, url
from testapp.models import *
from testapp.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sen.views.home', name='home'),
    url(r'^sen/','usrper.views.loginpage'),
    url(r'^signup/','usrper.views.spage'),
    url(r'^putindatabase/','usrper.views.signuppage'),
    url(r'^user/(\w+)/$', 'usrper.views.user_page'),
    url(r'^planner/', 'testapp.views.planner_view'),  
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^login/','usrper.views.loginpage'),  #for login page
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^logincheck/', 'usrper.views.check_login'), #for logincheck
    url(r'^logout/', 'usrper.views.logout'), #for logout
#    url(r'^home/<\w+>$', ),  #for the user loged in
    url(r'^home/','usrper.views.home'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
