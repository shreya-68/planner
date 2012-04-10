from django.contrib import admin
from sen.usrper.models import *
from sen.groups.models import *
from sen.timetable.models import *
from sen.newsfeeds.models import *

admin.site.register(students)
admin.site.register(group)
#admin.site.register(group_adm)
admin.site.register(groupmem)
#admin.site.register(group_ag)
admin.site.register(groupupdates)
admin.site.register(groupreq)
admin.site.register(courses)
admin.site.register(tttable)
admin.site.register(coursetostd)
admin.site.register(labttable)
#admin.site.register()


