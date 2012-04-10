from django import forms
from event.models import *
from django.forms.models import inlineformset_factory
from django.forms.widgets import SplitDateTimeWidget
import datetime

EventFormSet = inlineformset_factory(Pre_prep, Event, can_delete = False,exclude = ('start_time', 'end_time', 'pre_prep', 'user'))

class EventForm(forms.ModelForm):
    
    name = forms.CharField(max_length=40)
    datetime = forms.DateTimeField(widget = SplitDateTimeWidget, initial = datetime.datetime.now)
    venue = forms.CharField(max_length=40, required = False)
    duration = forms.DateTimeField(widget = SplitDateTimeWidget)
    #priority = forms.IntegerField(default = False)
    #remind = forms.BooleanField(default = False)

    class Meta:
        model = Event
        exclude = ('start_time', 'end_time', 'pre_prep', 'user')

class Event_typeForm(forms.ModelForm):
    class Meta:
        model = Event_Type
        exclude = ('id', 'priority')

class PrePrepForm(forms.ModelForm):
    pp_duration = forms.DateTimeField(widget = SplitDateTimeWidget, required = True)
    complete = forms.DateTimeField( widget = SplitDateTimeWidget, required = True)
    quantum_time = forms.DateTimeField( widget = SplitDateTimeWidget, required = True)
    max_eff = forms.DateTimeField( widget = SplitDateTimeWidget, required = True)
    class Meta:
        model = Pre_prep

#class LectureForm(forms.Model):
#    class Meta:
#        model = Lecture
#
#class ProjectForm(forms.Model):
#    class Meta:
#        model = Lecture
#
#class LectureForm(forms.Model):
#    class Meta:
#        model = Lecture
#
#SportForm = form_for_model(Sport)
#class LectureForm(forms.Model):
#    class Meta:
#        model = Lecture
#
#ClubForm = form_for_model(Club)
#
#OtherForm = form_for_model(Other)
#
#ExamForm = form_for_model(Exam)
