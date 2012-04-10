from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

#from usrper.models import *

#this following tables are related to the app sheduler 
#and calender
# Create your models here.
#class schedule(models.Model):
##	std_id = models.ForiegnKey('students.studentid')
#	activity = models.TextField()
#	start_time = models.TimeField('%H:%M')
#	stop_time = models.TimeField('%H:%M')
#
#
#class calender(models.Model):
##	std_id = models.ForiegnKey('students.studentid')
#	event = models.TextField()
#	stime = models.TimeField('%H:%M')
#	venue = models.TextField()
#	date  = models.DateField()
#

class Entry(models.Model):
    name = models.CharField(max_length = 40)
    description = models.CharField(max_length = 150, blank = True)
    start_time = models.DateTimeField()
    venue = models.CharField(max_length = 40)
    end_time = models.DateTimeField()
    pre_prep = models.BooleanField(default = False)
    remind = models.BooleanField(default = False)
    user = models.ForeignKey(User, blank = True, null = True)

    def __unicode__(self):
        if self.name:
        	return unicode(self.user) + u" - " + self.name
        else:
            return unicode(self.user) + u" - " + self.description[:40]

    def desc(self):
        if self.description:
            return "<i>%s</i> - %s" % (self.name, self.description)
        else:
        	return self.name
    desc.allow_tags = True

    class Meta:
        verbose_name_plural = "entries"


class EntryAdmin(admin.ModelAdmin):
    list_display = ["user", "start_time", "name", "description"]
    list_filter = ["user"]
    


