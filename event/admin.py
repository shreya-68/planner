from django.contrib import admin
from event.models import *

admin.site.register(Other)
admin.site.register(Pre_prep)
admin.site.register(Lecture)
admin.site.register(Project)
admin.site.register(Exam)
admin.site.register(Sport)
admin.site.register(Course)
admin.site.register(CourseLecture)
admin.site.register(Club)
admin.site.register(Event, EventAdmin)
admin.site.register(Event_Type, Event_typeAdmin)
