from django.db import models
#from usrper.models import *

#this following tables are related to the app sheduler 
#and calender
# Create your models here.
class schedule(models.Model):
#	std_id = models.ForiegnKey('students.studentid')
	activity = models.TextField()
	start_time = models.TimeField('%H:%M')
	stop_time = models.TimeField('%H:%M')


class calender(models.Model):
#	std_id = models.ForiegnKey('students.studentid')
	event = models.TextField()
	stime = models.TimeField('%H:%M')
	venue = models.TextField()
	date  = models.DateField()
    


