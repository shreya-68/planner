from django.db import models

class Event_Type(models.Model):
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
    priority = models.IntegerField()
    def __unicode__(self):
        return self.get_event_type_display()

class Event(models.Model):
    duration = models.TimeField(None)
    pre_prep = models.BooleanField()
    name = models.CharField(max_length=40)
    datetime = models.DateTimeField()
    venue = models.CharField(max_length=40)
    complete = models.FloatField(null=True)
    priority = models.IntegerField(default=0)

class Course(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    prof = models.CharField(max_length=20)
    credits = models.FloatField(None)

class Lecture(models.Model):
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
    slot = models.IntegerField(choices=SLOT_CHOICES)
    course = models.ForeignKey(Course)
    Type = models.ForeignKey(Event_Type)
    event = models.ForeignKey(Event)
    USER_DIFF_CHOICES = (
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
    )       
    user_difficulty = models.IntegerField(choices=USER_DIFF_CHOICES)

class Project(models.Model):
    course = models.ForeignKey(Course)
    Type = models.ForeignKey(Event_Type)
    event = models.ForeignKey(Event) 
    USER_DIFF_CHOICES = (
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
    )       
    user_difficulty = models.IntegerField(choices=USER_DIFF_CHOICES)

class Sport(models.Model):
        
    USER_DIFF_CHOICES = (
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
    )       
    user_difficulty = models.IntegerField(choices=USER_DIFF_CHOICES)
    Type = models.ForeignKey(Event_Type)
    event = models.ForeignKey(Event) 
        
class Exam(models.Model):
        
    Type = models.ForeignKey(Event_Type)
    event = models.ForeignKey(Event) 
    course = models.ForeignKey(Course)
    USER_DIFF_CHOICES = (
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
    )       
    user_difficulty = models.IntegerField(choices=USER_DIFF_CHOICES)


class Club(models.Model):
    club_name = models.CharField(max_length=40)
    Type = models.ForeignKey(Event_Type)
    event = models.ForeignKey(Event)
    USER_DIFF_CHOICES = (
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
    )       
    user_difficulty = models.IntegerField(choices=USER_DIFF_CHOICES)
    

class Other(models.Model):
   #event = models.ForeignKey(Events)
    Type = models.ForeignKey(Event_Type)
    event = models.ForeignKey(Event)
    #USER_DIFF_CHOICES = (
     #       (1,1),
      #      (2,2),
       #     (3,3),
        #    (4,4),
         #   (5,5),
    #)       
    #user_difficulty = models.IntegerField(choices=USER_DIFF_CHOICES)

# Create your models here.
