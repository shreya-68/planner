from django.contrib import admin
from groups.models import *

admin.site.register(group)
admin.site.register(groupmem)
admin.site.register(groupupdates)
admin.site.register(groupreq)
