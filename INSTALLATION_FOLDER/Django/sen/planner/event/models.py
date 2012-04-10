from django.db import models
from django.forms import ModelForm
from django import forms
import datetime
#from datetime import datetime
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.

class Event_Type(models.Model):
    id = models.IntegerField(primary_key = True)
    EVENT_CHOICES = (
            (u'P', 'Project'),
            (u'C', 'Club'),
            (u'L', 'Lecture'),
            (u'A', 'Assignment'),
            (u'O', 'Other'),
            (u'E', 'Exam'),
            (u'S', 'Sport'),
            (u'M', 'Meal'),
    )
    event_type = models.CharField(max_length=2, choices=EVENT_CHOICES)
    priority = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.get_event_type_display()

class Pre_prep(models.Model):
    pp_duration = models.DateTimeField()
    complete = models.DateTimeField(default = 0)
    quantum_time = models.DateTimeField(default = 0)
    max_eff = models.DateTimeField()

class Event(models.Model):
    name = models.CharField(max_length=40)
    datetime = models.DateTimeField()
    venue = models.CharField(max_length=40)
    duration = models.DateTimeField(None)
    pp = models.BooleanField()
    pre_prep = models.ForeignKey(Pre_prep, blank = True, null = True, on_delete=models.SET_NULL)
    priority = models.IntegerField(default = 0)
    remind = models.BooleanField(default = False)
    user = models.ForeignKey(User, blank = True, null = True)
    start_time = models.DateTimeField(auto_now_add = True)
    end_time = models.DateTimeField(blank = True, null = True)
    USER_DIFF_CHOICES = (
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
    )       
    user_difficulty = models.IntegerField(default = 1, choices=USER_DIFF_CHOICES)

    def __unicode__(self):
        if self.name:
        	return unicode(self.user) + u" - " + self.name
        else:
            return unicode(self.user) + u" - " + self.datetime

    class Meta:
        verbose_name_plural = "events"
    

class Course(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length = 20)
    prof = models.CharField(max_length=20)
    credits = models.FloatField(default = 4)
    SLOT_CHOICES = (
            (1, 1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
            (6,6),
            (7,7),
            (8,8),
    )
    slot = models.IntegerField(default = 1, choices=SLOT_CHOICES)

class Lecture(models.Model):
    course = models.ForeignKey(Course)
    Type = models.ForeignKey(Event_Type)
    event = models.ForeignKey(Event)

class Project(models.Model):
    course = models.ForeignKey(Course)
    Type = models.ForeignKey(Event_Type)
    event = models.ForeignKey(Event) 

class Sport(models.Model):
        
    Type = models.ForeignKey(Event_Type)
    event = models.ForeignKey(Event) 
        
class Exam(models.Model):
        
    Type = models.ForeignKey(Event_Type)
    event = models.ForeignKey(Event) 
    course = models.ForeignKey(Course)


class Club(models.Model):
    club_name = models.CharField(max_length=40)
    Type = models.ForeignKey(Event_Type)
    event = models.ForeignKey(Event)
    

class Other(models.Model):
   #event = models.ForeignKey(Events)
    Type = models.ForeignKey(Event_Type)
    event = models.ForeignKey(Event)


class EventAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "datetime", "duration", "priority", "remind"]
    list_filter = ["user"]

class Event_typeAdmin(admin.ModelAdmin):
    list_display = ["event_type", "priority"]








