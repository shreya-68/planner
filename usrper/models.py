from django.db import models
from django import forms
from django.forms.widgets import SplitDateTimeWidget
from event.models import *
import datetime
#from sen.timetable import *
#this file has user's personal information as well as academic info of a user
# Create your models here.
class students(models.Model):
	first_name = models.TextField()
	last_name = models.TextField()
	emailid = models.EmailField()
	phonenumber = models.BigIntegerField(max_length = 10)
	sleephours = models.DateTimeField(null=True)
	lunchtime = models.DateTimeField(null=True)
	dinnertime = models.DateTimeField(null=True)
	wakeup = models.DateTimeField(null=True)
	cpi = models.FloatField(null=True)
	cursem = models.IntegerField(null=True)
	year = models.IntegerField(null = True)
	studentid = models.IntegerField(primary_key=True, max_length = 9)
	cemailid =models.EmailField()
	#studentornot = models.

class UserEdit(models.Model):
    user = models.ForeignKey(students)
    edit = models.BooleanField()
# table showing the projectrelationtostudent
class UserCourses(models.Model):
    user = models.ForeignKey(students)
    course = models.ForeignKey(Course)

class test(models.Model):
    xyz = models.IntegerField()

class UserForm(forms.ModelForm):
    class Meta:
        model = students
        fields = ('first_name','last_name', 'studentid', 'phonenumber', 'cemailid') 

class ProfileForm(forms.ModelForm):
    sleephours = forms.DateTimeField(widget = SplitDateTimeWidget)
    lunchtime = forms.DateTimeField(widget = SplitDateTimeWidget)
    dinnertime = forms.DateTimeField(widget = SplitDateTimeWidget)
    wakeup = forms.DateTimeField(widget = SplitDateTimeWidget)
    cpi = forms.FloatField(required = False)
    class Meta:
        model = students
        fields = ('first_name', 'last_name', 'phonenumber', 'cemailid','sleephours', 'lunchtime', 'dinnertime', 'wakeup', 'cpi', 'cursem', 'year')
