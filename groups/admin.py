from django.contrib import admin
from groups.models import *

admin.site.register(group)
admin.site.register(groupmem)
admin.site.register(groupreq)
admin.site.register(groupevent)
