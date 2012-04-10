from django.contrib import admin
from schedule.models import *

admin.site.register(Entry, EntryAdmin)
