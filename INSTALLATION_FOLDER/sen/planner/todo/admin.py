
from django.contrib import admin
from todo.models import *

admin.site.register(Item, ItemAdmin)
admin.site.register(Datetime, DateAdmin)
