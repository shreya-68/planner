from django.db import models
#from sen.timetable import *
#this file has user's personal information as well as academic info of a user
# Create your models here.
class students(models.Model):
	name = models.TextField()
	emailid = models.EmailField()
	roomno = models.IntegerField(null=True)
	phonenumber = models.IntegerField()
	sleephours = models.TimeField('%H:%M',null=True)
	lunchtime = models.TimeField('%H:%M',null=True)
	dinnertime = models.TimeField('%H:%M',null=True)
	usualwakingtime = models.TimeField('%H:%M',null=True)
	hobbies = models.TextField(null=True)
	cpi = models.IntegerField(null=True)
	cursem = models.IntegerField(null=True)
	Year = models.IntegerField(null = True)
	studentid = models.IntegerField(primary_key=True)
	cemailid =models.EmailField()
	#studentornot = models.

# table showing the projectrelationtostudent
class stdtopro(models.Model):
	projectname = models.TextField()
	members = models.OneToOneField(students)
	diffbyuser = models.IntegerField()		#requires list of difficulty levels
	prodis = models.TextField()
