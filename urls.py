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
    url(r'^event/(?P<event_type_id>\d+)/(?P<event_id>\d+)/$', 'event.views.view_event_detail'),
    url(r'^event/(?P<event_type_id>\d+)/$','event.views.event_type_detail'),
    url(r'^event/delete/(?P<eid>\d+)/$','event.views.delete_event'),
    url(r'^event/$', 'event.views.all_events'), 
    #url(r'^plan/create/$','event.views.enter_date'),
    url(r'^plan/$', 'event.views.plan'),
    #url(r'^plan/date/$', 'event.views.plan_date'),
    url(r'^plan/create/$', 'event.views.create_plan'),
    url(r'^test/$', 'event.views.test'),
    #url(r'^plan/create/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$','event.views.create_plan'),
    url(r'^calendar/$', 'schedule.views.view_year'),
    url(r'^calendar/(?P<year>\d+)/$', 'schedule.views.view_year'),
    url(r'^calendar/month/(?P<year>\d+)/(?P<month>\d+)/$', 'schedule.views.view_month'),
    url(r'^calendar/month/(?P<year>\d+)/(?P<month>\d+)/(?P<change>(prev|next))/$', 'schedule.views.view_month'),
    url(r'^calendar/month/$', 'schedule.views.view_month'),
    url(r'^calendar/day/$', 'schedule.views.view_day'),
    url(r'^calendar/day/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'schedule.views.view_day'),
    url(r'^calendar/day/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<change>(prev|next))/$', 'schedule.views.view_day'),
    url(r'^calendar/day/add/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$', 'schedule.views.add_event_to_date'),
    url(r'^addevent/$', 'event.views.add_event'),
    url(r'^delete_event/(?P<eid>\d+)/$', 'event.views.delete_event'),
    url(r'^edit_event/(?P<eid>\d+)/$', 'event.views.edit_event'),
    #forum:
    url(r'^forum/$', 'forum.views.main'),
    url(r'^forum/(\d+)/$', 'forum.views.forum'),
    url(r'^forum/thread/delete/(\d+)/$', 'forum.views.delete_thread'),
    url(r'^thread/(\d+)/$', 'forum.views.thread'),
    url(r'^add_thread/(?P<pk>\d+)/$', 'forum.views.new_thread'),
    url(r'^post/(new_thread|reply)/(\d+)/$', 'forum.views.post'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    #groups:
    url(r'^groups/$', 'groups.views.show_group'),
    url(r'^groups/(?P<gid>\d+)/$', 'groups.views.show_group'),
    url(r'^groups/(?P<gid>\d+)/reject/$', 'groups.views.delete_request'),
    url(r'^groups/delete_members/(?P<gid>\d+)/$', 'groups.views.delete_members'),
    url(r'^groups/delete_members/(?P<gid>\d+)/(?P<mid>\d+)/$', 'groups.views.delete_member'),
    url(r'^groups/delete/(?P<gid>\d+)/$', 'groups.views.delete_group'),
    url(r'^groups/delete/event/(?P<eid>\d+)/$', 'groups.views.delete_event'),
    url(r'^groups/send_request/(?P<gid>\d+)/$', 'groups.views.send_request'),
    url(r'^accept/(?P<gid>\d+)/(?P<mid>\d+)/$', 'groups.views.join_group'),
    url(r'^groups/getmembers/(?P<gid>\d+)/', 'groups.views.get_members'),   
    url(r'^groups/edit/(?P<gid>\d+)/$', 'groups.views.edit_group'),   
    url(r'^groups/join_group/(?P<gid>\d+)/$', 'groups.views.join_group'),   
    url(r'^groups/addgroup/$', 'groups.views.create_group'),
    url(r'^groups/addevent/(?P<gid>\d+)/$', 'groups.views.add_event'),
    url(r'^groups/addtopic/(?P<gid>\d+)/$', 'groups.views.create_topic'),
    url(r'^groups/events/(?P<gid>\d+)/$', 'groups.views.show_events'),


    #url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^sen/','usrper.views.loginpage'),
    url(r'^signup/','usrper.views.spage'),
    url(r'^create_profile/','usrper.views.create_profile'),
    url(r'^putindatabase/','usrper.views.signuppage'),
    url(r'^user/(\w+)/$', 'usrper.views.user_page'),
    url(r'^login/','usrper.views.loginpage'),  #for login page
    url(r'^logincheck/', 'usrper.views.check_login'), #for logincheck
    url(r'^logout/', 'usrper.views.log_out'), #for logout
    url(r'^profile/', 'usrper.views.view_profile'), #for logout
    url(r'^create_profile/$', 'usrper.views.create_profile'), #for logout
    url(r'^edit_courses/$', 'usrper.views.edit_courses'), #for logout
#    url(r'^home/<\w+>$', ),  #for the user loged in
    url(r'^home/','usrper.views.home'),
    #url(r'','usrper.views.home'),


    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^settings/', 'schedule.views.settings'),
)
