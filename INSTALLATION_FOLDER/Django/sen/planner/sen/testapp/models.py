from django.db import models
from usrper.models import *

#this following tables are related to the app sheduler 
#and calender
# Create your models here.
class shedule(models.Model):
	std_id = models.OneToOneField(students)
	activity = models.TextField()
	start_time = models.TimeField('%H:%M')
	stop_time = models.TimeField('%H:%M')


class calender(models.Model):
	std_id = models.OneToOneField(students)
	event = models.TextField()
	stime = models.TimeField('%H:%M')
	venue = models.TextField()
	date  = models.DateField()
