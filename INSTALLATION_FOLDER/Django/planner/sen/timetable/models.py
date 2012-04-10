from django.db import models
from sen.usrper.models import *
#this table is for creating a timetable which is specific to a user
# Create your models here.
class courses(models.Model):
   courseid = models.CharField(max_length = 5)
   instid = models.IntegerField()
   slotid = models.IntegerField(blank=False)
   coursedis = models.TextField()
   coursename = models.TextField()
class tttable(models.Model):
   stime = models.TimeField('%H:%M')
   sptime = models.TimeField('%H:%M')
   slotnum = models.IntegerField(blank=False)
   day = models.TextField()
class coursetostd(models.Model):
   studentid = models.OneToOneField(students)
   courseid = models.OneToOneField(courses)
#class userhascourses(models.Model):
#	studentid = models.OneToOneField(students)
#	courseid = models.OneToOneField(courses)
class labttable(models.Model):
   labstime = models.TimeField()
   labstptime = models.TimeField()
   Courseid = models.ForeignKey('courses')
   #labgrpid =models.ForeignKey('')
   labday = models.TextField()

